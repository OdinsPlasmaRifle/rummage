import uuid
from logging import getLogger
from datetime import timedelta, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import JSONField, ArrayField
from enumfields import EnumField

from drf_mtg_card_crawler.enums import SearchStatus
from drf_mtg_card_crawler.exceptions import (
    SearchAlreadyProcessingError, SearchMaxRetriesExceededError
)
import drf_mtg_card_crawler.tasks as tasks
import drf_mtg_card_crawler.stores


logger = getLogger('django')


class DateModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Store(DateModel):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique=True, db_index=True)
    website = models.CharField(max_length=250)

    def search(self, term):
        return getattr(drf_mtg_card_crawler.stores, self.slug)(term)
        # results.reverse()
        # return results


class SearchResult(DateModel):
    term = models.ForeignKey(
        'drf_mtg_card_crawler.SearchTerm',
        related_name='results',
        on_delete=models.CASCADE
    )
    store = models.ForeignKey(
        'drf_mtg_card_crawler.Store', on_delete=models.CASCADE
    )
    url = models.CharField(max_length=250)
    metadata = JSONField(null=True, default=dict)
    expires = models.DateTimeField()
    # Override created to support manually setting the field.
    created = models.DateTimeField(default=now, db_index=True)

    MAX_CACHE_AGE = 600

    class Meta:
        ordering = ['created']


class SearchTerm(DateModel):
    search = models.ForeignKey(
        'drf_mtg_card_crawler.Search',
        related_name='terms',
        on_delete=models.CASCADE
    )
    term = models.CharField(max_length=150, db_index=True)

    class Meta:
        ordering = ['created']


class Search(DateModel):
    identifier = models.UUIDField(
        unique=True,
        db_index=True,
        default=uuid.uuid4
    )
    stores = models.ManyToManyField('drf_mtg_card_crawler.Store')
    retries = models.IntegerField(default=0)
    status = EnumField(
        SearchStatus,
        max_length=50,
        default=SearchStatus.QUEUED,
        db_index=True
    )

    # Max number of retries allowed.
    MAX_RETRIES = 3

    def get_stores(self):
       return self.stores.all() if self.stores.all().exists() \
            else Store.objects.all()

    def get_cachable_results(self, term, store, nocache=False):
        """
        Get any search results that could be used as a cache source.
        """

        if nocache:
            return SearchResult.objects.none()

        return SearchResult.objects.filter(
            term__term=term.term,
            store=store,
            expires__gt=now(),
        ).distinct("url").order_by("url", "created")

    def process_async(self):
        tasks.process_search.delay(self.id)

    def process(self):
        """
        Process a search in the following manner:

        1. Check that the search is not getting processed already.
        2. Change the search status to processing.
        3. Loop through each search term
            a. Create a pool and futures for this term.
            a. Loop through each store.
                - Use cachable results if any exist.
                - Add search functions (for the store) to the "term" pool and
                  process them in parallel.
            b. Collect results as they are returned by the parallel searches.
            d. Save all results on the search using a bulk create.
        4. Finalize the search status.
        """

        try:
            if self.status == SearchStatus.PROCESSING:
                raise SearchAlreadyProcessingError()

            # Set the status as processing.
            self.status = SearchStatus.PROCESSING
            self.save(update_fields=["status", "updated",])

            # Get stores.
            stores = self.get_stores()

            # Get expiry dates.
            cache_expires = now() + timedelta(
                seconds=SearchResult.MAX_CACHE_AGE
            )
            no_cache_expires = now()

            search_results = []
            for term in self.terms.all():
                # Define pools for parallelism.
                term_pool = ThreadPoolExecutor(5)
                term_futures = []

                for store in stores:
                    # Get results that can be used as a cache base.
                    cachable_results = self.get_cachable_results(term, store)

                    if cachable_results.exists():
                        # Cachable search results exist, copy them.
                        for cachable_result in cachable_results:
                            search_results.append(
                                SearchResult(
                                    term=term,
                                    store=store,
                                    url=cachable_result.url,
                                    metadata=cachable_result.metadata,
                                    expires=no_cache_expires,
                                    created=cachable_result.created
                                )
                            )
                    else:
                        def _parallel_search(store, term, expires):
                            p_results = []
                            for s_result in store.search(term.term):
                                p_results.append(
                                    SearchResult(
                                        term=term,
                                        store=store,
                                        expires=expires,
                                        **s_result
                                    )
                                )
                            return p_results

                        term_futures.append(
                            term_pool.submit(
                                _parallel_search, store, term, cache_expires
                            )
                        )

                for x in as_completed(term_futures):
                    search_results.extend(x.result())

            # Add search results.
            SearchResult.objects.bulk_create(search_results)

        except Exception as exc:
            # Handle retries.
            retries = self.retries + 1
            if retries > self.MAX_RETRIES:
                exc = SearchMaxRetriesExceededError()
                self.status = SearchStatus.FAILED
                self.save(update_fields=["status", "updated",])
                raise exc

            self.retries = retries
            self.status = SearchStatus.QUEUED
            self.save(update_fields=["status", "updated",])
            raise exc

        else:
            self.status = SearchStatus.COMPLETE
            self.save(update_fields=["status", "updated"])

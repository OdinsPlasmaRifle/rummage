import uuid
from logging import getLogger

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

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


class SearchTerm(DateModel):
    search = models.ForeignKey(
        'drf_mtg_card_crawler.Search',
        related_name='terms',
        on_delete=models.CASCADE
    )
    term = models.CharField(max_length=150, db_index=True)


class Search(DateModel):
    identifier = models.UUIDField(
        unique=True,
        db_index=True,
        default=uuid.uuid4
    )
    stores = models.ManyToManyField('drf_mtg_card_crawler.Store')

    def process(self):
        stores = self.stores.all() if self.stores.all().exists() \
            else Store.objects.all()

        search_results = []
        for term in self.terms.all():
            for store in stores:
                for result in store.search(term.term):
                    search_results.append(
                        SearchResult(
                            term=term,
                            store=store,
                            **result
                        )
                    )

        SearchResult.objects.bulk_create(search_results)

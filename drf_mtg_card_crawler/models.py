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
    slug = models.CharField(max_length=250)
    website = models.CharField(max_length=250)

    def search(self, term):
        return getattr(drf_mtg_card_crawler.stores, self.slug)(term)


class SearchResult(DateModel):
    search = models.ForeignKey(
        'drf_mtg_card_crawler.Search',
        related_name='results',
        null=True,
        on_delete=models.CASCADE
    )
    term = models.CharField(max_length=150)
    stores = models.ManyToManyField('drf_mtg_card_crawler.Store')


class Search(DateModel):
    # Terms to search by.
    terms = ArrayField(
        models.CharField(max_length=150), size=500, null=True, blank=True
    )
    # Stores to include in the search.
    stores = models.ManyToManyField('drf_mtg_card_crawler.Store')

    def save(self, *args, **kwargs):
        created = True if not self.id else False

        # Save the search details.
        super().save(*args, **kwargs)

        if created:
            stores = self.stores if self.stores.all().exists() \
                else Store.objects.all()

            for term in self.terms:
                search_result = SearchResult.objects.create(
                    search=self,
                    term=term
                )

                stores_found = []
                for store in stores:
                    if store.search(term):
                        stores_found.append(store)

                search_result.stores.set(stores_found)

from logging import getLogger

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


logger = getLogger('django')


class DateModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Store(DateModel):
    name = models.CharField(max_length=250)
    website = models.CharField(max_length=250)
    search_url = models.CharField(max_length=250)


class SearchResult(DateModel):
    search = models.ForeignKey(
        'drf_mtg_card_crawler.Search',
        related_name='results',
        null=True,
        on_delete=models.CASCADE
    )
    term = ArrayField(
        models.CharField(max_length=150), size=500, null=True, blank=True
    )
    stores = models.ManyToManyField('drf_mtg_card_crawler.Store')


class Search(DateModel):
    # Terms to search by.
    terms = ArrayField(
        models.CharField(max_length=150), size=500, null=True, blank=True
    )
    # Stores to include in the search.
    stores = models.ManyToManyField('drf_mtg_card_crawler.Store')

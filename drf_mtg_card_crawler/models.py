from logging import getLogger

from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField


logger = getLogger('django')


class DateModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

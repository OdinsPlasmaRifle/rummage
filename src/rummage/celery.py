from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

if not os.environ.get("DJANGO_SETTINGS_MODULE", ''):
    os.environ.setdefault(
    	"DJANGO_SETTINGS_MODULE", "rummage.settings"
    )

app = Celery('rummage')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

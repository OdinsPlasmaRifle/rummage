import logging
from datetime import timedelta, datetime

from django.utils.timezone import now
from celery import shared_task


logger = logging.getLogger('django')


"""
Maintenance
"""

@shared_task
def clear_searches():
    """
    Task to clear searches on a sechdule.
    """

    from drf_mtg_card_crawler.models import Search

    state_change_date_from = now() - timedelta(days=7)
    # Round about method to call delete because limit cannot be used on deletes.
    pks = Search.objects.filter(
        created__lt=state_change_date_from
    ).values_list('pk')[:10000]
    Search.objects.filter(pk__in=pks).delete()


"""
Tasks
"""


@shared_task(acks_late=True, bind=True, max_retries=11, default_retry_delay=10)
def process_search(self, search_id):
    """
    Process a search in the background.
    """

    from drf_mtg_card_crawler.models import Search
    from drf_mtg_card_crawler.exceptions import SearchFatalError

    try:
        search = Search.objects.get(id=search_id)
    except BuildTask.DoesNotExist:
        logger.error('Search does not exist.')
        return

    try:
        search.process()
    except SearchFatalError as exc:
        logger.exception(exc)
    except Exception:
        self.retry(max_retries=Search.MAX_RETRIES)

import logging

from celery import shared_task


logger = logging.getLogger('django')


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

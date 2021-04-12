from rest_framework import status
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


class RummageException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_error_slug = 'internal_error'

    def __init__(self, detail=None, error_slug=None):
        if detail is not None:
            self.detail = force_text(detail)
            self.error_slug = force_text(error_slug)
        else:
            self.detail = force_text(self.default_detail)
            self.error_slug = force_text(self.default_error_slug)

    def __str__(self):
        return self.detail


class SearchError(RummageException):
    default_detail = 'Search error.'
    default_error_slug = 'search_error'


class SearchFatalError(SearchError):
    default_detail = 'Search fatal error.'
    default_error_slug = 'search_fatal_error'


class SearchAlreadyProcessingError(SearchFatalError):
    default_detail = 'Search already processing.'
    default_error_slug = 'search_already_processing_error'


class SearchMaxRetriesExceededError(SearchFatalError):
    default_detail = 'Search max retries exceeded.'
    default_error_slug = 'search_max_retries_exceeded_error'

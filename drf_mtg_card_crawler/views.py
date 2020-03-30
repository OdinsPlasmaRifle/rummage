from logging import getLogger

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from rest_framework.pagination import LimitOffsetPagination

from .serializers import SearchSerializer
from .models import Search


logger = getLogger('django')


class CreateSearchesView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SearchSerializer
    pagination_class = LimitOffsetPagination
    page_size = 100


class SearchesView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SearchSerializer

    def get_object(self):
        try:
            return Search.objects.get(id=self.kwargs['id'])
        except Search.DoesNotExist:
            raise exceptions.NotFound()

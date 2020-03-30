from logging import getLogger

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import SearchSerializer, CreateSearchSerializer
from .models import Search


logger = getLogger('django')


class CreateSearchView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SearchSerializer
    pagination_class = LimitOffsetPagination
    page_size = 100

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateSearchSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            self.serializer_class(
                serializer.instance, context=self.get_serializer_context()
            ).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class SearchView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SearchSerializer

    def get_object(self):
        try:
            return Search.objects.get(id=self.kwargs['id'])
        except Search.DoesNotExist:
            raise exceptions.NotFound()

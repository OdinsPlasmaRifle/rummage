from logging import getLogger

from rest_framework import serializers, exceptions

from .models import Store, Search, SearchResult


logger = getLogger('django')


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('id', 'name', 'created', 'updated',)


class SearchResultSerializer(serializers.ModelSerializer):
    stores = StoreSerializer(read_only=True, many=True)

    class Meta:
        model = SearchResult
        fields = ('term', 'stores', 'created', 'updated',)
        read_only = ('term', 'stores', 'created', 'updated',)


class SearchSerializer(serializers.ModelSerializer):
    results = SearchResultSerializer(read_only=True, many=True)

    class Meta:
        model = Search
        fields = ('id', 'terms', 'results', 'created', 'updated',)
        read_only = ('id', 'results', 'created', 'updated',)

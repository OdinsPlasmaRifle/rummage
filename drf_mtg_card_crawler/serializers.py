from logging import getLogger

from rest_framework import serializers, exceptions

from .models import Store, Search, SearchResult


logger = getLogger('django')


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('id', 'name', 'website',)
        read_only_fields = ('id', 'name', 'website',)


class SearchResultSerializer(serializers.ModelSerializer):
    stores = StoreSerializer(read_only=True, many=True)

    class Meta:
        model = SearchResult
        fields = ('term', 'stores',)
        read_only_fields = ('term', 'stores',)


class SearchSerializer(serializers.ModelSerializer):
    results = SearchResultSerializer(read_only=True, many=True)

    class Meta:
        model = Search
        fields = ('id', 'terms', 'results', 'created', 'updated',)
        read_only_fields = ('id', 'results', 'created', 'updated',)

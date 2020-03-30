from logging import getLogger

from django.db import transaction
from rest_framework import serializers, exceptions

from .models import Store, Search, SearchTerm, SearchResult


logger = getLogger('django')


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('id', 'name', 'website',)
        read_only_fields = ('id', 'name', 'website',)


class SearchResultSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)

    class Meta:
        model = SearchResult
        fields = ('store', 'url', 'metadata',)
        read_only_fields = ('store', 'url', 'metadata',)


class SearchTermSerializer(serializers.ModelSerializer):
    results = SearchResultSerializer(read_only=True, many=True)

    class Meta:
        model = SearchTerm
        fields = ('term', 'results',)
        read_only_fields = ('term', 'results',)


class SearchSerializer(serializers.ModelSerializer):
    terms = SearchTermSerializer(read_only=True, many=True)

    class Meta:
        model = Search
        fields = ('id', 'terms', 'terms', 'created', 'updated',)
        read_only_fields = ('id', 'terms', 'created', 'updated',)


class CreateSearchSerializer(SearchSerializer):
    terms = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        write_only=True,
        min_length=1,
        max_length=100
    )

    def create(self, validated_data):
        with transaction.atomic():
            terms = validated_data.pop("terms", [])
            search = Search.objects.create(**validated_data)

            for term in terms:
                SearchTerm.objects.create(search=search, term=term)

        search.process()
        return search

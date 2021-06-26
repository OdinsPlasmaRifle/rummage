from logging import getLogger

from django.db import transaction
from rest_framework import serializers, exceptions

from .models import Store, Search, SearchError, SearchTerm, SearchResult


logger = getLogger('django')


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = ('id', 'name', 'slug', 'website',)
        read_only_fields = ('id', 'name', 'slug', 'website',)


class SearchErrorSerializer(serializers.ModelSerializer):
    store = serializers.IntegerField(source="store.id")

    class Meta:
        model = SearchError
        fields = ('store', 'error',)
        read_only_fields = ('store', 'error',)


class SearchResultSerializer(serializers.ModelSerializer):
    store = serializers.IntegerField(source="store.id")

    class Meta:
        model = SearchResult
        fields = ('store', 'url', 'name', 'image', 'price',)
        read_only_fields = ('store', 'url', 'name', 'image', 'price',)


class SearchTermSerializer(serializers.ModelSerializer):
    errors = SearchErrorSerializer(read_only=True, many=True)
    results = SearchResultSerializer(read_only=True, many=True)

    class Meta:
        model = SearchTerm
        fields = ('term', 'errors', 'results',)
        read_only_fields = ('term', 'errors', 'results',)


class SearchSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source="identifier")
    status = serializers.CharField(source="status.value", read_only=True)
    terms = SearchTermSerializer(read_only=True, many=True)

    class Meta:
        model = Search
        fields = ('id', 'status', 'terms', 'created', 'updated',)
        read_only_fields = (
            'id', 'status', 'terms', 'created', 'updated',
        )


class CreateSearchSerializer(SearchSerializer):
    status = serializers.CharField(source="status.value", read_only=True)
    stores = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        max_length=100
    )
    terms = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        write_only=True,
        min_length=1,
        max_length=100
    )

    class Meta:
        model = Search
        fields = (
            'id', 'status', 'retries', 'stores', 'terms', 'created', 'updated',
        )
        read_only_fields = ('id', 'status', 'retries', 'created', 'updated',)

    def validate_stores(self, stores):
        return Store.objects.filter(slug__in=stores, enabled=True)

    def create(self, validated_data):
        stores = validated_data.pop("stores", None)
        terms = validated_data.pop("terms", [])

        # Get default stores.
        if stores is None:
            stores = Store.objects.filter(enabled=True)

        with transaction.atomic():
            search = Search.objects.create(**validated_data)
            search.stores.set(stores)
            for term in terms:
                SearchTerm.objects.create(search=search, term=term)

        search.process_async()
        return search

from django.urls import include, path, re_path
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_spectacular.views import (
    SpectacularJSONAPIView, SpectacularSwaggerView
)

from . import views


admin.autodiscover()

v1_api_urlpatterns = [
    re_path(
        r'^stores/?$', views.ListStoreView.as_view(), name='stores'
    ),
    re_path(
        r'^stores/(?P<id>\w+)/?$', views.StoreView.as_view(), name='stores-view'
    ),
    re_path(
        r'^searches/?$', views.CreateSearchView.as_view(), name='searches'
    ),
    re_path(
        r'^searches/(?P<id>([a-zA-Z0-9\_\-]+))/?$',
        views.SearchView.as_view(),
        name='searches-view'
    ),
]

namespaced_urlpatterns = [
    re_path(
        r'^1/', include((v1_api_urlpatterns, 'rummage'), namespace='1')
    )
]

urlpatterns = [
    # Administration
    re_path(r'^admin/', admin.site.urls),

    # Index
    re_path(
      r'^$', TemplateView.as_view(template_name="index.html"), name='index'
    ),

    # Documentation
    re_path(
        r'^schema.json$',
        SpectacularJSONAPIView.as_view(
            api_version='1',
            urlconf=namespaced_urlpatterns,
            custom_settings={
                'TITLE': 'Rummage API',
                'DESCRIPTION': """
The **Rummage API** is a product searcher for MTG stores in South Africa.
                    """,
                'VERSION': '1',
            }
        ),
        name='schema'
    ),
    re_path(
        r'^swagger/?$',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    # API
    re_path(r'^', include((namespaced_urlpatterns, 'rummage')))
]

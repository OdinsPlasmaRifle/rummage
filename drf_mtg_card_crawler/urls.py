from django.urls import include, path, re_path
from django.contrib import admin
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views


admin.autodiscover()

schema_view = get_schema_view(
   openapi.Info(
      title="MtG Card Crawler",
      default_version='v1',
      description=""
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Administration
    re_path(r'^admin/', admin.site.urls),

    # Swagger
    re_path(
      r'^swagger(?P<format>\.json|\.yaml)$',
      schema_view.without_ui(cache_timeout=None),
      name='schema-json'
    ),
    re_path(
      r'^swagger/$',
      schema_view.with_ui('swagger', cache_timeout=None),
      name='schema-swagger-ui'
    ),
    re_path(
      r'^$',
      schema_view.with_ui('redoc', cache_timeout=None),
      name='schema-redoc'
    ),

    # API
    re_path(r'^searches/?$', views.CreateSearchView.as_view(), name='searches'),
    re_path(r'^searches/(?P<id>([a-zA-Z0-9\_\-]+))/?$', views.SearchView.as_view(), name='searches-view'),
]
from logging import getLogger

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework import exceptions


logger = getLogger('django')

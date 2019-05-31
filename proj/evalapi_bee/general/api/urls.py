from django.conf.urls import url, include
from rest_framework import routers

from general.api import views  # NOQA F401

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
]

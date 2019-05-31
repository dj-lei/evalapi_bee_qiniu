from django.conf.urls import url, include
from rest_framework import routers

from deal_records.api import views  # NOQA F401

urlpatterns = [
    url(r'^v1/deal-records/$', views.FakeDealRecordView.as_view()),
]

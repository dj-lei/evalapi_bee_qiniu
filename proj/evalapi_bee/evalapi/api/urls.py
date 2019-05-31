from django.conf.urls import url, include
from rest_framework import routers

from evalapi.api import views  # NOQA F401

router = routers.SimpleRouter()
router.register('evaluation', views.EvaluationView, base_name='evaluation')
router.register('price-history', views.PriceTrendView, base_name='price_history')
router.register('future-price', views.FuturePriceTrendView, base_name='future-price')
router.register('residual-price', views.ResidualPriceTrendView, base_name='residual-price')

urlpatterns = [
    url(r'^v1/', include(router.urls)),
]

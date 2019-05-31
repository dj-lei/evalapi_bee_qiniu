from django.conf.urls import url, include
from django.conf import settings


urlpatterns = [
    url(r'^api/evalapi/', include('evalapi.api.urls')),
    url(r'^api/deal-history/', include('deal_records.api.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

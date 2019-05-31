import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "evalapi_bee.settings.dev")

application = get_wsgi_application()

from django.test import TestCase
from django.conf import settings

# Create your tests here.


class ExampleTestCase(TestCase):
    # load fixture from dumpdata in runtest.py
    fixtures = [settings.BASE_DIR + '/dj_fixture.json', '-i']

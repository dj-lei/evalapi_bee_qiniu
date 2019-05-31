import json
from urllib.parse import urlencode

from django.test import TestCase
from django.conf import settings

# Create your tests here.


class DealRecordTestCase(TestCase):
    # pass
    # load fixture from dumpdata in runtest.py
    fixtures = [settings.BASE_DIR + '/dj_fixture.json', '-i']

    def test_deal_records_can_fetch_correctly(self):
        payload = {
            'model_detail_slug': '4805_ah',
            'city': '成都'
        }
        params = urlencode(payload)
        res = self.client.get('/api/deal-history/v1/deal-records/?' + params,
                              headers={'content_type': 'application/json'})
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 200, data)




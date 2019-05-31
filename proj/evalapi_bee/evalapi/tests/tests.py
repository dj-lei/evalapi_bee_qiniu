from urllib.parse import urlencode
import datetime
import json

from django.test import TestCase
from django.conf import settings
# Create your tests here.


class UtilsTestCase(TestCase):
    # load fixture from dumpdata in runtest.py
    # fixtures = [settings.BASE_DIR + '/dj_fixture.json', '-i']
    def test_days_can_convert_to_datetime_correctly(self):
        from evalapi.utils import days2datetime
        import datetime
        seq = [-720, -420, -360,  -90, 0, 60, 360, 420, 720]
        res_seq = [days2datetime(day, base_datetime=datetime.datetime(year=2017, month=11, day=11)) for day in seq]
        self.assertEqual(datetime.datetime(2015, 11, 11), res_seq[0])
        self.assertEqual(datetime.datetime(2016, 9, 11), res_seq[1])
        self.assertEqual(datetime.datetime(2016, 11, 11), res_seq[2])
        self.assertEqual(datetime.datetime(2017, 8, 11), res_seq[3])
        self.assertEqual(datetime.datetime(2017, 11, 11), res_seq[4])
        self.assertEqual(datetime.datetime(2018, 1, 11), res_seq[5])
        self.assertEqual(datetime.datetime(2018, 11, 11), res_seq[6])
        self.assertEqual(datetime.datetime(2019, 1, 11), res_seq[7])
        self.assertEqual(datetime.datetime(2019, 11, 11), res_seq[8])

    def test_month_diff_can_work_correctly(self):
        from evalapi.utils import month_diff
        today = datetime.date.today()
        months = month_diff(today, today)
        self.assertEqual(months, 1)
        months = month_diff(datetime.date(2017, 12, 1), datetime.date(2018, 1, 1))
        self.assertEqual(months, 1)


class EvalApiTest(TestCase):
    def test_evaluation_when_online_date_equals_target_date(self):
        td = datetime.date.today()
        payload = {
            'model_detail_slug': 'model_25023_cs',
            'city': '成都',
            'mile': 10,
            'online_year': td.year,
            'online_month': td.month
        }
        s = urlencode(payload)
        res = self.client.get('/api/evalapi/v1/evaluation/?' + s, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_eval_price_api_can_get_value_correctly(self):
        payload = {
            'model_detail_slug': 'model_25023_cs',
            'city': '成都',
            'mile': 10,
            'online_year': 2017,
            'online_month': 9
        }
        s = urlencode(payload)
        res = self.client.get('/api/evalapi/v1/evaluation/?' + s, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_price_history_can_get_value_correctly(self):
        payload = {
            'model_detail_slug': 'model_25023_cs',
            'city': '成都',
            'mile': 10,
            'online_year': 2017,
            'online_month': 9
        }
        s = urlencode(payload)
        res = self.client.get('/api/evalapi/v1/price-history/?' + s, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_future_price_can_get_value_correctly(self):
        payload = {
            'model_detail_slug': 'model_25023_cs',
            'city': '成都',
            'mile': 10,
            'online_year': 2017,
            'online_month': 9
        }
        s = urlencode(payload)
        res = self.client.get('/api/evalapi/v1/future-price/?' + s, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_current_month_can_evaluate_correctly(self):
        payload = {
            'model_detail_slug': 'model_25023_cs',
            'city': '成都',
            'mile': 10,
            'online_year': 2018,
            'online_month': 1
        }
        s = urlencode(payload)
        res = self.client.get('/api/evalapi/v1/price-history/?' + s, content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 200, data.get('detail'))

    def test_residual_prices(self):
        payload = {
            'model_detail_slug': 'model_25023_cs',
            'city': '成都',
            'mile': 10,
            'online_year': 2018,
            'online_month': 1
        }
        s = urlencode(payload)
        res = self.client.get('/api/evalapi/v1/residual-price/?' + s, content_type='application/json')
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 200, data.get('detail'))





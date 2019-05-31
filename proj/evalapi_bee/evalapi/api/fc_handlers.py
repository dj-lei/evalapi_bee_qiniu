from time import perf_counter
import json
import sys
import os
import logging
from io import StringIO
import traceback

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if path not in sys.path:
    sys.path.insert(0, path)

from django.conf import settings
from django.core.wsgi import get_wsgi_application

DEBUG = bool(os.environ.get('DEBUG', 0))
if DEBUG:
    os.environ['VALUATE_RUNTIME_ENVIRONMENT'] = 'LOCAL'
settings.configure(DEBUG=DEBUG)
application = get_wsgi_application()

from raven import Client
from rest_framework import exceptions as exc

from evalapi import serializers
from evalapi import error_handers
from evalapi import services

LOGGER = logging.getLogger()
if settings.DEBUG:
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(logging.StreamHandler())
else:
    raven_client = Client('http://d496222377bb4a899d13b5e711023277:d0a6efdf07e44cd0a5ec04d39f3e4df8@exception.eyelee.cn/38')


def function_handler(time_log=True):
    def func_wrap(func):
        def wrapped(e, c=None):
            t = perf_counter()
            try:
                query_param = json.loads(e)
            except json.JSONDecodeError as e:
                query_param = dict()

            try:
                result = func(query_param, c)
            except Exception as e:
                if not isinstance(e, exc.APIException):
                    errors = StringIO()
                    traceback.print_exc(file=errors)
                    s = errors.getvalue().replace('\n', ' ')
                    LOGGER.error('%s' % s)
                    raise e
                return error_handers.exception_handler(e, dict())
            if time_log:
                elapsed_ms = round(((perf_counter() - t) * 1000), 2)
                LOGGER.info('%.2f %s' % (elapsed_ms, e))

            return result

        return wrapped
    return func_wrap


@function_handler()
def evaluation(query_param, context):
    ser = serializers.EvalSerialzier(data=query_param)
    ser.is_valid(raise_exception=True)

    return ser.data['result']


@function_handler()
def monthly_history(query_param, context):
    ser = serializers.EvalPriceTrend(data=query_param)
    ser.is_valid(raise_exception=True)

    return ser.data['result']


@function_handler()
def future_price(query_param, context):
    ser = serializers.EvalFuturePrice(data=query_param)
    ser.is_valid(raise_exception=True)

    return ser.data['result']


@function_handler()
def residual_price(query_param, context):
    ser = serializers.EvalResidualPrice(data=query_param)
    ser.is_valid(raise_exception=True)

    return ser.data['result']


@function_handler()
def handle_model_detail(query_param, context):
    services.EvalService.handle_model_details()


if __name__ == '__main__':
    import fc2

    def invoke_fc(service_name, function_name, payload=None, invocation_type='Sync',
                  log_type='None', trace_id=None, key='LTAIZtlslPls3GEn', secret='EFE5Byj2r1aO6RPbTem5mUBFOz3klS'):
        endpoint = '30691700.cn-beijing.fc.aliyuncs.com'
        client = fc2.Client(accessKeyID=key, accessKeySecret=secret,
                            endpoint=endpoint, invocation_type=invocation_type)

        payload_bin = bytes(json.dumps(payload), encoding='utf-8') if payload else None
        res = client.invoke_function(service_name, function_name, payload=payload_bin)
        res_data = json.loads(res.data, encoding='utf-8')
        return res_data

        pass


    param = {"model_detail_slug": "m4755_ba", "city": "葫芦岛", "online_month": 7, "mile": 11.0,
     "online_year": 2008}
    # param = {'model_detail_slug': u'4d4b4e48be_autotis', 'city': '杭州', 'online_month': 3, 'mile': 0.3, 'online_year': 2018}
    # param = {
    #     'model_detail_slug': '4931_ah',
    #     'city': '兰州',
    #     'mile': 10,
    #     'online_year': 2010,
    #     'online_month': 5
    # }
    s = bytes(json.dumps(param), encoding='utf-8')
    # res = evaluation(s)
    # print(res)
    # res = future_price(s)
    # print(res)
    # res = monthly_history(s)
    # res = monthly_history(s)
    res = residual_price(s)

    print(res)
    # invoke_fc('evalapi', 'evaluation', payload=param)

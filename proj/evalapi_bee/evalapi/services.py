import datetime
import os
from dateutil.relativedelta import relativedelta
# from valuate.conf import global_settings as gl

DEBUG = bool(os.environ.get('DEBUG', 1))
if DEBUG:
    os.environ['VALUATE_RUNTIME_ENVIRONMENT'] = 'LOCAL'

from valuate.predict.predict_api import Predict
from valuate.exception import api_error as vexec
import pymysql

from evalapi import exceptions as exc
from evalapi import utils




class EvalService:
    @classmethod
    def _split_details(cls, details, copy=50):
        result = list()
        for i in range(copy):
            result.append(details[i::copy])
        return result

    @classmethod
    def handle_model_details(cls):
        DEBUG = bool(int(os.environ.get('DEBUG', False)))
        predict = Predict()
        if DEBUG:
            conn = pymysql.connect(host="101.200.229.249", port=3306, user='pingjia', password='De32wsxC',
                                   database='pingjia', autocommit=False)
        else:
            conn = pymysql.connect(host="100.114.30.239", port=18056, user='pingjia', password='De32wsxC',
                                   database='pingjia', autocommit=False)
        details = predict.load_valuated_model_details()

        SET_MODEL_DETAIL_D = '''
        update open_model_detail set status='D' where status != 'A'
        '''

        MODEL_DETAIL_SQL = """
        update open_model_detail set status='Y' where listed_year >= (year(now()) - 19) and detail_model_slug in ({slugs})
        """

        SET_MODEL_D = '''
        update open_category set status='D' where status != 'A'
        '''

        SET_MODEL_Y = '''
            UPDATE open_category
            SET status = 'Y'
            WHERE parent IS NOT NULL AND slug IN (
              SELECT tmp.slug
              FROM (
                     SELECT oc.slug
                     FROM open_category oc, open_model_detail omd
                     WHERE omd.global_slug = oc.slug AND omd.status = 'Y'
                     GROUP BY oc.slug
                     HAVING count(*) > 0
                   ) AS tmp)
        '''

        SET_BRAND_Y = '''
            UPDATE open_category
            SET status = 'Y'
            WHERE slug IN (
              SELECT slug
              FROM (
                     SELECT brand.slug
                     FROM open_category model, open_category brand
                     WHERE brand.slug = model.parent AND brand.parent IS NULL AND model.status = 'Y'
                     GROUP BY brand.slug
                     HAVING count(*) > 0) AS tmp)
        '''
        details_str = ["'%s'" % detail for detail in details]
        splited = cls._split_details(details_str)
        conn.begin()
        try:
            with conn.cursor() as cursor:
                # cursor.execute(SET_MODEL_DETAIL_D)

                for item in splited:
                    DETAIL = MODEL_DETAIL_SQL.format(slugs=','.join(item))
                    cursor.execute(DETAIL)

                # cursor.execute(SET_MODEL_D)
                cursor.execute(SET_MODEL_Y)
                cursor.execute(SET_BRAND_Y)
                conn.commit()
        except Exception as e:
            conn.rollback()
        finally:
            conn.close()

    @classmethod
    def eval_deal_price(cls, model_detail_slug, city, mile, online_date, target_date):
        p = Predict()
        try:
            result = p.predict(
                city=city, model_detail_slug=model_detail_slug,
                reg_year=online_date.year, reg_month=online_date.month,
                deal_year=target_date.year, deal_month=target_date.month, mile=mile
            )
        except vexec.ApiParamsValueError as e:
            raise exc.EvalApiException(code=exc.VALUATION_ERROR_MAP[e.name])

        res = dict()
        for item in result:
            k = item.pop('intent')
            res[k] = item

        return res

    @classmethod
    def price_in_past_six_month(cls, model_detail_slug, city, mile, online_date, target_date):
        p = Predict()
        try:
            result = p.history_price_trend(
                city=city, mile=mile, model_detail_slug=model_detail_slug,
                reg_year=online_date.year, reg_month=online_date.month,
                deal_year=target_date.year, deal_month=target_date.month
            )
        except vexec.ApiParamsValueError as e:
            raise exc.EvalApiException(code=exc.VALUATION_ERROR_MAP[e.name])
        res = dict()

        for item in result:
            tp = item.pop('type')
            cd = item.pop('condition')
            res[tp] = [(utils.month_diff2date(int(month)).strftime('%Y-%m'), price)
                       for month, price in list(item.items())[:6]]
        # res['condition'] = cd
        return res

    @classmethod
    def price_in_next_three_years(cls, model_detail_slug, city, mile, online_date, target_date):
        p = Predict()
        try:
            result = p.future_price_trend(
                city=city, mile=mile, model_detail_slug=model_detail_slug,
                reg_year=online_date.year, reg_month=online_date.month,
                deal_year=target_date.year, deal_month=target_date.month
            )
        except vexec.ApiParamsValueError as e:
            raise exc.EvalApiException(code=exc.VALUATION_ERROR_MAP[e.name])
        res = dict()

        for item in result:
            tp = item.pop('type')
            cd = item.pop('condition')
            res[tp] = {utils.month_diff2date(int(month)).strftime('%Y'): price
                       for month, price in list(item.items())[0:]}
        # res['condition'] = cd
        return res

    @classmethod
    def price_in_next_six_month(cls, model_detail_slug, city, mile, online_date, target_date):
        predict = Predict()
        res_dict = dict()
        result = predict.residuals(city=city, model_detail_slug=model_detail_slug, reg_year=online_date.year,
                                   reg_month=online_date.month,
                                   deal_year=target_date.year, deal_month=target_date.month,
                                   mile=mile)
        for item in result:
            prices = [item[str(i)] for i in range(13)]
            res_dict.setdefault(item['intent'], dict())[item['condition']] = prices
        return res_dict


def days2datetime(days, base_datetime=None):
    base_datetime = datetime.datetime.now() if not base_datetime else base_datetime

    month_diff = int(days / 30)

    return base_datetime + relativedelta(months=month_diff)

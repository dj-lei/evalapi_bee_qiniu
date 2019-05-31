from datetime import date

from rest_framework import serializers  # NOQA F401
from djchoices import DjangoChoices, ChoiceItem

from evalapi import exceptions as exc
from evalapi import services
from evalapi import utils


class IntentChoice(DjangoChoices):
    sell = ChoiceItem('sell')
    buy = ChoiceItem('buy')
    release = ChoiceItem('release')
    private = ChoiceItem('private')
    lowest = ChoiceItem('lowest')
    cpo = ChoiceItem('cpo')
    replace = ChoiceItem('replace')
    auction = ChoiceItem('auction')
    avg_buy = ChoiceItem('avg-buy')
    avg_sell = ChoiceItem('avg-sell')


class ConditionChoice(DjangoChoices):
    excellent = ChoiceItem('excellent')
    good = ChoiceItem('good')
    fair = ChoiceItem('fair')
    bad = ChoiceItem('bad')


class EvalSerialzier(serializers.Serializer):
    model_detail_slug = serializers.SlugField(max_length=50, required=True, write_only=True)
    city = serializers.CharField(max_length=20, required=True, write_only=True)
    mile = serializers.FloatField(required=True, help_text=u'万公里', min_value=0, write_only=True)
    online_year = serializers.IntegerField(required=True, write_only=True)
    online_month = serializers.IntegerField(required=True, min_value=1, max_value=12, write_only=True)
    target_year = serializers.IntegerField(required=False, write_only=True)
    target_month = serializers.IntegerField(required=False, write_only=True)
    trans_times = serializers.IntegerField(required=False)

    result = serializers.DictField(read_only=True)

    def validate_target_date(self, attrs):
        now = date.today()
        online_date = date(year=attrs['online_year'], month=attrs['online_month'], day=1)
        target_date = date(year=attrs.get('target_year', now.year),
                           month=attrs.get('target_month', now.month), day=1)

        if online_date > target_date:
            raise serializers.ValidationError(detail='上牌时间超过当前时间')

        # if target_date == online_date:
        #     target_date = date(year=target_date.year, month=target_date.month+1, day=1)

        return online_date, target_date

    def validate(self, attrs):
        online_date, target_date = self.validate_target_date(attrs)

        res = services.EvalService.eval_deal_price(
            attrs['model_detail_slug'], city=attrs['city'],
            mile=attrs['mile'], online_date=online_date,
            target_date=target_date
        )
        attrs['result'] = res

        return attrs


class EvalPriceTrend(EvalSerialzier):

    def validate(self, attrs):
        online_date, target_date = self.validate_target_date(attrs)
        # used_month = utils.month_diff(online_date, target_date)

        res = services.EvalService.price_in_past_six_month(
            attrs['model_detail_slug'], city=attrs['city'],
            mile=attrs['mile'], online_date=online_date,
            target_date=target_date
        )
        attrs['result'] = res

        return attrs


class EvalFuturePrice(EvalSerialzier):

    def validate(self, attrs):
        online_date, target_date = self.validate_target_date(attrs)

        res = services.EvalService.price_in_next_three_years(
            attrs['model_detail_slug'], city=attrs['city'],
            mile=attrs['mile'], online_date=online_date,
            target_date=target_date
        )
        attrs['result'] = res

        return attrs


class EvalResidualPrice(EvalSerialzier):

    def validate(self, attrs):
        online_date, target_date = self.validate_target_date(attrs)

        res = services.EvalService.price_in_next_six_month(
            attrs['model_detail_slug'], city=attrs['city'],
            mile=attrs['mile'], online_date=online_date,
            target_date=target_date
        )
        attrs['result'] = res

        return attrs

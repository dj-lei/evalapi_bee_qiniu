# coding:utf-8
import asyncio

from rest_framework import serializers  # NOQA F401
from django.core import  exceptions as dj_exc

from deal_records import models
from category import models as cate_models
from deal_records import exceptions as exc
from deal_records import services


class CarDealHistorySerializer(serializers.ModelSerializer):
    deal_time = serializers.SerializerMethodField()
    deal_type = serializers.SerializerMethodField()

    def get_deal_type(self, obj):
        deal_type = {
            'sell_dealer': 'sell',
            'private_party': 'private',
            'buy_dealer': 'buy',
            'buy_cpo': 'buy'
        }.get(obj.deal_type, obj.deal_type)

        return deal_type

    def get_deal_time(self, obj):
        try:
            deal_time_str = obj.deal_time.strftime('%Y-%m-%d')
            return deal_time_str
        except Exception as e:
            import traceback
            traceback.print_exc()
            return ''

    class Meta:
        model = models.CarDealHistory
        fields = ['deal_time', 'deal_type', 'price', 'city']


class DealCount(serializers.ModelSerializer):
    date = serializers.DateField(format='%Y-%m')

    class Meta:
        model = models.CarDealHistoryStatatics
        fields = ['date', 'count']


class DealHistorySerializer(serializers.Serializer):
    model_detail_slug = serializers.CharField(max_length=20, required=True, write_only=True)
    city = serializers.CharField(max_length=20, required=True, write_only=True)

    deal_records = CarDealHistorySerializer(many=True)
    deal_counts = DealCount(many=True)

    def validate_model_detail_slug(self, value):
        q_dmodel = cate_models.ModelDetail.objects.filter(detail_model_slug=value).prefetch_related('global_slug')
        try:
            obj = q_dmodel[0]
        except IndexError:
            raise exc.DealRecordException(code=exc.DealRecordErrorCode.BAD_MODEL_DETAIL_SLUG)
        return obj

    def validate(self, attrs):
        import time
        a = time.perf_counter()
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)



        model_detail = attrs['model_detail_slug']
        async def _get_deal_records():
            return services.DealHistoryService.get_deal_records(
                model_detail.detail_model_slug, attrs['city']
            )

        async def _get_deal_counts():
            return services.DealHistoryService.get_history_deal_count(
                model_detail.global_slug.slug,
                attrs['city']
            )
        tasks = [asyncio.ensure_future(_get_deal_records()), asyncio.ensure_future(_get_deal_counts())]

        loop.run_until_complete(asyncio.wait(tasks))

        attrs['deal_records'] = tasks[0].result()
        attrs['deal_counts'] = tasks[1].result()

        # model_detail = attrs['model_detail_slug']
        # attrs['deal_records'] = services.DealHistoryService.get_deal_records(
        #     model_detail.detail_model_slug, attrs['city']
        # )
        # attrs['deal_counts'] = services.DealHistoryService.get_history_deal_count(
        #     model_detail.global_slug.slug,
        #     attrs['city']
        # )
        print('%.2f' % ((time.perf_counter() - a) * 1000))

        return attrs

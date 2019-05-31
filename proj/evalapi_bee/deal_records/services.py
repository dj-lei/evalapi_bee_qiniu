# coding: utf-8
from django.core.cache import cache

from general import models as gen_models
from deal_records import models


class DealHistoryService:
    @classmethod
    def get_deal_records(cls, model_detail_slug, city):
        cities = get_same_area_cities(city)
        cur_city = models.CarDealHistory.objects.filter(
            city=city,
            price__isnull=False,
            model_detail_slug=model_detail_slug
        ).order_by('-deal_time')
        l_cur_city = cur_city.count()
        if l_cur_city >= 10:
            history = cur_city[:10]
        else:
            other_city = models.CarDealHistory.objects.filter(
                city__in=cities,
                price__isnull=False,
                model_detail_slug=model_detail_slug
            ).exclude(city=city).order_by('-deal_time')
            history = list(cur_city[:l_cur_city]) + list(other_city[:10-l_cur_city+1])

        return list(history)

    @classmethod
    def get_history_deal_count(cls, model_slug, city):
        stats = models.CarDealHistoryStatatics.objects.filter(
            city=city,
            model_slug=model_slug
        ).order_by('date')

        return list(stats)


def get_same_area_cities(city):
    key = 'cities_in_same_area_%s' % city

    cities = cache.get(key, None)
    if not cities:
        city = gen_models.City.objects.get(name=city, parentid__isnull=False)
        cities = gen_models.City.objects.filter(area=city.area).values('name')
        cities = [c['name'] for c in cities]
        cache.set(key, cities)

    return cities

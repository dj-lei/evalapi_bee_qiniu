from django.db import models  # NOQA F401

# Create your models here.


class City(models.Model):
    """
    省份/城市表(只读)
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    pinyin = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    quhao = models.CharField(max_length=32, blank=True, null=True, db_index=True)
    url = models.URLField()
    parentid = models.ForeignKey('City', null=True, db_column='parentid', related_name='cities',
                                 verbose_name=u'parent use id')
    priority = models.IntegerField(null=True)
    longitude = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    latitude = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    area = models.CharField(max_length=5, verbose_name=u'区域')
    city_administration_number = models.IntegerField(null=True, verbose_name="城市行政区号")

    class Meta:
        db_table = 'open_city'



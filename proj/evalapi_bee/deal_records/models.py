# coding:utf-8

from django.db import models  # NOQA F401


class CarDealHistory(models.Model):
    """ Car deal product data."""

    DEAL_TYPE_CHOICES = (
        ('sell_dealer', '商家收购'),
        ('trade_in', '置换'),
        ('auction', '拍卖'),
        ('private_party', '个人交易'),
        ('buy_dealer', '商家零售'),
        ('buy_cpo', '认证二手车'),
    )

    brand_zh = models.CharField(max_length=32, blank=True, null=True,
                                verbose_name='品牌名称')
    model_zh = models.CharField(max_length=32, blank=True, null=True,
                                verbose_name='型号名称')
    model_detail_zh = models.CharField(max_length=50, blank=True, null=True,
                                       verbose_name='款型名称')
    brand_slug = models.CharField(max_length=32, blank=True, null=True,
                                  db_index=True, verbose_name='品牌slug')
    model_slug = models.CharField(max_length=32, blank=True, null=True,
                                  db_index=True, verbose_name='型号slug')
    model_detail_slug = models.CharField(max_length=32, blank=True, null=True,
                                         db_index=True, verbose_name='款型slug')
    year = models.IntegerField(blank=True, default=0, db_index=True,
                               verbose_name='初次上牌年份')
    month = models.IntegerField(blank=True, default=6,
                                verbose_name='初次上牌月份')
    mile = models.DecimalField(max_digits=5, decimal_places=2, blank=True,
                               null=True, verbose_name='行驶里程', help_text='单位万公里')
    volume = models.DecimalField(max_digits=5, decimal_places=1, blank=True,
                                 null=True, verbose_name='排量', db_index=True)
    color = models.CharField(max_length=32, blank=True, null=True,
                             verbose_name='颜色')
    control = models.CharField(max_length=32, blank=True, null=True,
                               verbose_name='变速箱')
    province = models.CharField(max_length=50, blank=True, null=True,
                                db_index=True, verbose_name='省份')
    city = models.CharField(max_length=50, blank=True, null=True,
                            db_index=True, verbose_name='城市')
    deal_time = models.DateTimeField(blank=True, null=True, db_index=True,
                                     verbose_name='成交时间')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,
                                null=True, verbose_name='成交价格')
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES,
                                 blank=True, null=True, verbose_name='交易方式')
    source = models.CharField(max_length=50, blank=True, null=True,
                              verbose_name='历史成交数据来源')

    class Meta:
        db_table = 'car_deal_history'
        verbose_name = '二手车成交历史数据'


class CarDealHistoryStatatics(models.Model):
    model_slug = models.CharField(max_length=32, null=True, verbose_name='型号')
    city = models.CharField(max_length=50, null=True, verbose_name='城市')
    date = models.DateField(null=True, verbose_name='日期')
    count = models.IntegerField(null=True, verbose_name='数量')

    class Meta:
        db_table = 'car_deal_history_statatics'


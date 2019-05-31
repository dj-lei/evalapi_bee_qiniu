# coding=utf-8

from django.db import models

from category.managers import (
    BrandManager, ModelManager, ModelDetailManager, DefaultManager
)


class Category(models.Model):
    """ 品牌/型号
    只读
    """
    CLASSIFIED_CHOICE = (
        (u'微型车', u'微型车'),
        (u'小型车', u'小型车'),
        (u'紧凑型车', u'紧凑型车'),
        (u'中型车', u'中型车'),
        (u'中大型车', u'中大型车'),
        (u'豪华型车', u'豪华型车'),
        (u'小型SUV', u'小型SUV'),
        (u'紧凑型SUV', u'紧凑型SUV'),
        (u'中型SUV', u'中型SUV'),
        (u'中大型SUV', u'中大型SUV'),
        (u'全尺寸SUV', u'全尺寸SUV'),
        (u'MPV', u'MPV'),
        (u'跑车', u'跑车'),
        (u'微面', u'微面'),
        (u'微卡', u'微卡'),
        (u'轻客', u'轻客'),
        (u'皮卡', u'皮卡'),
    )
    STATUS_CHOICE = (
        ('A', u'ADD 刚添加的品牌或型号'),
        ('Y', u'YES 确定投入使用的品牌或型号'),
        ('D', u'DELETE 标记为需要删除的品牌或型号'),
    )

    ATTRIBUTE_CHOICE = (
        (u'合资', u'合资'),
        (u'进口', u'进口'),
        (u'国产', u'国产'),
    )

    POPULAR_CHOICE = (
        (u'A', u'畅销'),
        (u'B', u'一般'),
        (u'C', u'冷门'),
    )

    name = models.CharField(max_length=50, blank=True, null=True, default='name', verbose_name=u'型号/品牌（中文名）')
    first_letter = models.CharField(max_length=1, blank=True, null=True, verbose_name=u'首字母')
    slug_global = models.CharField(max_length=32, blank=True, null=True)
    slug = models.CharField(max_length=32, blank=True, null=True, unique=True, verbose_name=u'型号/品牌（英文简写）')
    parent = models.ForeignKey('Category', to_field='slug', db_column='parent',
                               max_length=32, blank=True, null=True,
                               db_constraint=False, related_name='models',
                               verbose_name=u'品牌（英文简写）')
    mum = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'厂商')
    classified = models.CharField(max_length=32, blank=True, null=True, choices=CLASSIFIED_CHOICE, verbose_name=u'级别')
    keywords = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    logo_img = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'缩略图')
    pinyin = models.CharField(max_length=32, blank=True, null=True, db_index=True, verbose_name=u'型号/品牌（拼音）')
    status = models.CharField(max_length=1, blank=True, null=True, default='A', choices=STATUS_CHOICE)
    attribute = models.CharField(max_length=10, blank=True, null=True, db_index=True, choices=ATTRIBUTE_CHOICE,
                                 verbose_name=u'属性，区分国产还是进口等')
    units = models.IntegerField(default=0, verbose_name=u'参与统计的该型号车源数量')
    popular = models.CharField(max_length=1, blank=True, null=True, default='B', choices=POPULAR_CHOICE)
    score = models.IntegerField(default=0, verbose_name=u'百度搜索指数')
    alias = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'别名')
    brand_area = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'产地')

    class Meta:
        db_table = 'open_category'

    objects = DefaultManager()
    _brands = BrandManager()
    _models = ModelManager()

    def __unicode__(self):
        return self.slug

    __str__ = __unicode__

    def __repr__(self):
        return '<Category slug: %s id: %s>' % (self.slug, self.id)


class ModelDetail(models.Model):
    """ 款型
    只读
    """

    STATUS_CHOICE = (
        ('A', u'ADD 刚添加的款型'),
        ('Y', u'YES 确定可投入使用的款型'),
        ('D', u'DELETE 标记为需要删除的款型'),
    )
    HAS_PARAMS = (
        ('Y', u'YES 有配置参数信息'),
        ('N', u'NO 无配置参数信息'),
    )
    detail_model = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    detail_model_slug = models.CharField(max_length=50, blank=True, null=True, unique=True)
    price_bn = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    url = models.URLField(default='', blank=True, null=True, db_index=True)
    year = models.IntegerField(blank=True, default=0, verbose_name=u'年款')
    volume = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, verbose_name=u'排量')
    global_slug = models.ForeignKey(Category, to_field='slug', db_column='global_slug', blank=True, null=True,
                                    on_delete=models.SET_NULL, related_name='model_detail')
    domain = models.CharField(max_length=32, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True, default='A', choices=STATUS_CHOICE)
    has_param = models.CharField(max_length=1, blank=True, null=True, default='N', choices=HAS_PARAMS)
    listed_year = models.IntegerField(blank=True, default=0, verbose_name=u'上市年份')
    delisted_year = models.IntegerField(blank=True, null=True, verbose_name=u'退市年份')
    control = models.CharField(max_length=32, blank=True, null=True, db_index=True, verbose_name=u'变速箱')
    emission_standard = models.CharField(max_length=20, blank=True, null=True, db_index=True, verbose_name=u'排放标准')
    continuity_id = models.IntegerField(null=True, blank=True, verbose_name='款型系列id')
    vv = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True, verbose_name=u'虚拟排量')

    class Meta:
        db_table = 'open_model_detail'

    objects = ModelDetailManager()

    def __unicode__(self):
        return self.detail_model_slug

    __str__ = __unicode__

    def __repr__(self):
        return '<ModelDetail detail_model_slug: %s id: %s>' % (self.detail_model_slug, self.id)

from django.db import models


class DefaultManager(models.Manager):
    def get_queryset(self):
        return super(DefaultManager, self).get_queryset().filter(status='Y')


class BrandManager(models.Manager):
    def get_queryset(self):
        return super(BrandManager, self).get_queryset().filter(parent=None, status='Y')


class ModelManager(models.Manager):
    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(parent__isnull=False, status='Y')


class ModelDetailManager(models.Manager):
    def get_queryset(self):
        return super(ModelDetailManager, self).get_queryset().filter(status='Y')


class LevelVinNormalManager(models.Manager):
    def get_queryset(self):
        return super(LevelVinNormalManager, self).get_queryset().filter(status=LevelVinStatusChoices.normal)

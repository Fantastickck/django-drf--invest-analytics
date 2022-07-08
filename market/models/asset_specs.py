from django.db import models


class TypeAsset(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Тип актива'
        verbose_name_plural = 'Типы активов'

    def __str__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Сектор'
        verbose_name_plural = 'Секторы'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    iso_alpha_2 = models.CharField(max_length=2, verbose_name='ISO Alpha 2', null=True)
    iso_alpha_3 = models.CharField(max_length=3, verbose_name='ISO Alpha 3', null=True)
    iso_number = models.PositiveSmallIntegerField(verbose_name='ISO число', null=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.iso_alpha_3


class Market(models.Model):
    name = models.CharField(max_length=255, verbose_name='Биржа')

    class Meta:
        verbose_name = 'Биржа'
        verbose_name_plural = 'Биржи'

    def __str__(self):
        return self.name

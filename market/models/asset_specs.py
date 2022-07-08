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

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


class Market(models.Model):
    name = models.CharField(max_length=255, verbose_name='Биржа')

    class Meta:
        verbose_name = 'Биржа'
        verbose_name_plural = 'Биржи'

    def __str__(self):
        return self.name

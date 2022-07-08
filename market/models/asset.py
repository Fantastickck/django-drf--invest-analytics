from django.db import models

from .asset_specs import TypeAsset, Sector, Country, Market
from .currency import Currency


class Asset(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    ticker = models.CharField(max_length=10, verbose_name='Тикер')
    type_asset = models.ForeignKey(
        TypeAsset, on_delete=models.CASCADE, verbose_name='Тип актива')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание')
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name='Валюта')
    sector = models.ForeignKey(
        Sector, on_delete=models.SET_NULL, null=True, verbose_name='Сектор')
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, verbose_name='Страна')
    market = models.ForeignKey(
        Market, on_delete=models.SET_NULL, null=True, verbose_name='Биржа')

    class Meta:
        verbose_name = 'Актив'
        verbose_name_plural = 'Активы'

    def __str__(self):
        return self.ticker

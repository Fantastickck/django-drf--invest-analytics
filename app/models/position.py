from django.db import models

from market.models.asset import Asset
from .account import Account


class Position(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='positions', verbose_name='Счет')
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='positions', verbose_name='Актив')
    avg_price = models.DecimalField(
        max_digits=16, decimal_places=6, verbose_name='Средняя цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return f'{self.account.user.username} | {self.account.name} | {self.asset.name}'

from django.db import models
from app.services.account import get_result_currency_position

from market.models.asset import Asset
from market.models.currency import Currency
from .account import Account


class Position(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='positions', verbose_name='Счет')
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='positions', verbose_name='Актив')
    avg_price_usd = models.DecimalField(
        max_digits=16, decimal_places=6, verbose_name='Средняя цена USD')
    avg_price_rub = models.DecimalField(
        max_digits=16, decimal_places=6, verbose_name='Средняя цена RUB')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    commission = models.DecimalField(
        max_digits=16, decimal_places=6, verbose_name='Комиссии', default=0)

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def get_invested(self, currency):
        if currency.abbreviation == 'USD':
            return self.avg_price_usd * self.quantity
        return self.avg_price_rub * self.quantity

    def get_current_amount(self, currency, courses):
        last_price = get_result_currency_position(
            self, 
            self.asset.last_price, 
            currency_to=currency,
            currency_courses=courses
        )
        return last_price

    def __str__(self):
        return f'{self.account.user.username} | {self.account.name} | {self.asset.name}'


class CurrencyPosition(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE,
        related_name='currency_positions', verbose_name='Счет')
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Валюта')
    quantity = models.DecimalField(
        max_digits=16, decimal_places=6, verbose_name='Количество')
    avg_price_rub = models.DecimalField(
        max_digits=16, decimal_places=6, verbose_name='Средняя цена в RUB')
    avg_price_usd = models.DecimalField(
        max_digits=16, decimal_places=6, verbose_name='Средняя цена в USD')

    class Meta:
        verbose_name = 'Валютная позиция'
        verbose_name_plural = 'Валютные позиции'

    def __str__(self):
        return f'{self.account.user.username} | {self.account.name} | {self.asset.name}'

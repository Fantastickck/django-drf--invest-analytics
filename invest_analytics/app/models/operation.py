from datetime import datetime

from django.db import models

from .account import Account
from market.models import Asset, Currency


OPERATION_TYPE = (
    ('Купить', 'BUY'),
    ('Продать', 'SELL'),
    ('Пополнить', 'INPUT'),
    ('Вывести', 'OUTPUT'),
    ('Дивиденд', 'DIVIDEND'),
    ('Купон', 'COUPON')
)


class Operation(models.Model):
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='operations', verbose_name='Актив')
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='operations', verbose_name='Счет')
    price = models.DecimalField(
        max_digits=20, decimal_places=6, verbose_name='Средняя цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    commission = models.DecimalField(
        max_digits=12, decimal_places=6, default=0, verbose_name='Комиссия')
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, verbose_name='Валюта операции')
    type_operation = models.CharField(
        max_length=63, choices=OPERATION_TYPE, verbose_name='Тип операции')
    date = models.DateTimeField(
        default=datetime.today, verbose_name='Дата операции')

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'

    def __str__(self):
        return f'{self.date} | {self.asset.ticker} | {self.price*self.quantity}'

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название счета')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='accounts', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def get_total_amount(self, currency, courses):
        asset_amount = sum(
            position.get_current_amount(currency, courses)*position.quantity 
            for position in self.positions.all()
        )
        # currency_amount = sum(
        #     position.get_currenct_amount(currency) for position in self.currency_positions.all()
        # )
        return asset_amount


    def __str__(self):
        return f'{self.id} | {self.user}'


class AccountHistoricalModel(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='states')
    date = models.DateField(verbose_name='Дата состояния')
    total_invested = models.DecimalField(
        max_digits=20, decimal_places=6, verbose_name='Всего инвестировано')
    turnover = models.DecimalField(
        max_digits=20, decimal_places=6, verbose_name='Оборот средств')
    total_amount = models.DecimalField(
        max_digits=20, decimal_places=6, verbose_name='Общая стоимость')
    total_profit = models.DecimalField(
        max_digits=20, decimal_places=6, verbose_name='Общая прибыль')

    class Meta:
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'
        ordering = ['date']

    def __str__(self):
        return f'{self.account.id} | {self.date}'

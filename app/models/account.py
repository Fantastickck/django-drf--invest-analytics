from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название счета')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='accounts', verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'{self.user.username} | {self.name}'


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
        max_digits=20, decimal_places=6, verbose_name='Общая')

    class Meta:
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояния'

    def __str__(self):
        return f'{self.account} | {self.date}'

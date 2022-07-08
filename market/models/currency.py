from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    abbreviation = models.CharField(max_length=10, verbose_name='Аббревиатура')
    symbol = models.CharField(max_length=10, verbose_name='Символ')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.abbreviation

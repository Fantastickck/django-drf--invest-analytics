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

    
class CurrencyCourse(models.Model):
    currency_from = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currencies_from', verbose_name='Из валюты')
    currency_to = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currencies_to', verbose_name='В валюту')
    value = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='Курс')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return f'{self.currency_from}/{self.currency_to}'
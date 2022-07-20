from django.db import models


CURRENCY_TYPE = (
    ('CURRENCY', 'Обычная валюта'),
    ('CRYPTOCURRENCY', 'Криптовалюта')
)


class Currency(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование', unique=True)
    type_currency = models.CharField(max_length=20, choices=CURRENCY_TYPE, verbose_name='Тип валюты')
    abbreviation = models.CharField(max_length=10, verbose_name='Аббревиатура', unique=True)
    symbol = models.CharField(max_length=10, verbose_name='Символ')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.abbreviation

    
class CurrencyCourse(models.Model):
    currency_from = models.ForeignKey(
        Currency, 
        on_delete=models.CASCADE, 
        related_name='currencies_from', 
        verbose_name='Из валюты')
    currency_to = models.ForeignKey(
        Currency, on_delete=models.CASCADE, 
        related_name='currencies_to', 
        verbose_name='В валюту')
    value = models.DecimalField(
        max_digits=20, 
        decimal_places=6, 
        default=0.0,
        verbose_name='Курс')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return f'{self.currency_from}/{self.currency_to}'

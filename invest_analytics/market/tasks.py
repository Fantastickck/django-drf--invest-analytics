import os
from decimal import Decimal

from celery import shared_task
from tinkoff.invest import Client


from config import settings 
import django
django.setup()
from market.models.currency import Currency, CurrencyCourse


def get_usd_figi(client):
    currencies = client.instruments.currencies().instruments
    for currency in currencies:
        if currency.name == 'Доллар США':
            return currency.figi


def get_course(obj, nominal):
    price = obj.last_prices[0].price
    units = str(price.units)
    nano = str(price.nano)
    course = Decimal(f'{units}.{nano}')
    return course/nominal


@shared_task
def get_currency_courses():
    with Client(settings.TINVEST_TOKEN) as client:
        usd_figi = get_usd_figi(client)
        usd_rub = get_course(client.market_data.get_last_prices(figi=[usd_figi]), nominal=1)
        currency_rub = Currency.objects.get(abbreviation='RUB')
        currency_usd = Currency.objects.get(abbreviation='USD')
        currencies = client.instruments.currencies().instruments
        for currency in currencies:
            if 'RUB' in currency.ticker:
                currency_figi = currency.figi
                last_price = client.market_data.get_last_prices(figi=[currency_figi])
                nominal = currency.nominal.units
                course_to_rub = get_course(last_price, nominal)
                if course_to_rub != 0.0:
                    course_to_usd = course_to_rub/usd_rub
                    ticker = currency.ticker[0:3]
                    currency_from = Currency.objects.get(abbreviation=ticker)
                    ticker_rub = CurrencyCourse.objects.get_or_create(
                        currency_from=currency_from, 
                        currency_to=currency_rub, 
                    )[0]
                    ticker_rub.value =course_to_rub
                    ticker_rub.save()
                    ticker_usd = CurrencyCourse.objects.get_or_create(
                        currency_from=currency_from,
                        currency_to=currency_usd,
                    )[0]
                    ticker_usd.value = course_to_usd
                    ticker_usd.save()
    print('UPDATED CURRENCY COURSES')
                    # print(currency.name, currency.ticker)
                    # print(f'\t{ticker}/RUB: {course_to_rub}' )
                    # print(f'\t{ticker}/USD: {course_to_usd}')


if __name__ == '__main__':
    get_currency_courses()
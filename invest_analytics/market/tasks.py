from decimal import Decimal

from tinkoff.invest import Client

from config.celery import app
from config import settings

from market.models.currency import (
    Currency, 
)
from market.services_tasks.currency import (
    get_course,
    get_usd_figi,
    update_courses,
    update_usd_rub_courses
)


@app.task
def update_currency_courses() -> None:
    """Update courses for all currencies."""
    currency_rub = Currency.objects.get(abbreviation='RUB')
    currency_usd = Currency.objects.get(abbreviation='USD')
    with Client(settings.TINVEST_TOKEN) as client:
        usd_figi = get_usd_figi(client)
        usd_rub = get_course(client.market_data.get_last_prices(
            figi=[usd_figi]), nominal=1)
        currencies = client.instruments.currencies().instruments
        for currency in currencies:
            if 'RUB' in currency.ticker:
                last_price = client.market_data.get_last_prices(
                    figi=[currency.figi])
                nominal = currency.nominal.units
                course_to_rub = get_course(last_price, nominal)
                if course_to_rub != 0.0:
                    course_to_usd = Decimal(course_to_rub/usd_rub)
                    ticker = currency.ticker[0:3]
                    currency_from = Currency.objects.get(abbreviation=ticker)
                    update_courses(
                        currency_from=currency_from,
                        currency_rub=currency_rub,
                        currency_usd=currency_usd,
                        course_to_rub=course_to_rub,
                        course_to_usd=course_to_usd
                    )
    update_usd_rub_courses(
        usd_rub,
        currency_rub=currency_rub,
        currency_usd=currency_usd
    )

from decimal import Decimal

from tinkoff.invest import Client, schemas

from config.celery import app
from config import settings

from market.models.currency import Currency
from market.models.asset import Asset

from market.services_tasks.currency import (
    get_course,
    get_usd_figi,
    update_courses,
    update_usd_rub_courses
)
from market.services_tasks.generic import (
    get_figi,
    get_decimal_price
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


@app.task
def update_stock_last_prices() -> None:
    """Update last prices for stocks."""
    assets = Asset.objects.all()
    for asset in assets:
        with Client(settings.TINVEST_TOKEN) as client:
            try:
                figi = get_figi(client=client, ticker=asset.ticker, type_instrument='share')
            except:
                print('Does not exist ticker')
                continue
            lot = client.instruments.share_by(
                id_type=schemas.InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, 
                id=figi
            ).instrument.lot
            last_price = get_decimal_price(
                client.market_data.get_last_prices(figi=[figi]),
                lot=lot
            )            
            asset.last_price = last_price
            asset.save()

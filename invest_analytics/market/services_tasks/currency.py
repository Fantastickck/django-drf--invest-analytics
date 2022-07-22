from decimal import Decimal

from tinkoff.invest import Client

from market.models.currency import (
    Currency, 
    CurrencyCourse
)


def get_usd_figi(client: Client) -> str:
    currencies = client.instruments.currencies().instruments
    for currency in currencies:
        if currency.name == 'Доллар США':
            return currency.figi


def get_course(obj, nominal) -> Decimal:
    """Rebuild course from api to Decimal."""
    price = obj.last_prices[0].price
    units = str(price.units)
    nano = str(price.nano)
    course = Decimal(f'{units}.{nano}')
    return Decimal(course/nominal)


def update_usd_rub_courses(
    usd_rub: Decimal, 
    currency_rub: Currency, 
    currency_usd: Currency
) -> None:
    """Update courses: {ticker}/RUB and {ticker}/USD."""
    CurrencyCourse.objects\
        .filter(currency_from=currency_usd, currency_to=currency_rub)\
        .update(value=Decimal(usd_rub))
    CurrencyCourse.objects\
        .filter(currency_from=currency_rub, currency_to=currency_usd)\
        .update(value=Decimal(1/usd_rub))

    
def update_courses(
    currency_from: Currency,
    currency_rub: Currency,
    currency_usd: Currency,
    course_to_rub: Decimal,
    course_to_usd: Decimal
) -> None:
    """Update courses: USD/RUB and RUB/USD."""
    CurrencyCourse.objects.update_or_create(
        currency_from=currency_from,
        currency_to=currency_rub,
        defaults={'value': course_to_rub}
    )
    CurrencyCourse.objects.update_or_create(
        currency_from=currency_from,
        currency_to=currency_usd,
        defaults={'value': course_to_usd}
    )

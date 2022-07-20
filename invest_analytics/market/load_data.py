from tinkoff.invest import Client

from config import settings

from market.models.currency import Currency

def load_currencies() -> None:
    with Client(settings.TINVEST_TOKEN) as client:
        currencies = client.instruments.currencies().instruments
        for currency in currencies:
            ticker = currency.ticker[0:3]
            Currency.objects.get_or_create(
                abbreviation=ticker, 
                defaults={'name': currency.name, 'type_currency': 'CURRENCY'}
            )

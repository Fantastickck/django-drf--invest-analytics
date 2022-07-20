from tinkoff.invest import Client

from config import settings
import django
django.setup()

from market.models.currency import Currency

def load_currencies() -> None:
    with Client(settings.TINVEST_TOKEN) as client:
        currencies = client.instruments.currencies().instruments
        for currency in currencies:
            ticker = currency.ticker[0:3]
            try:
                Currency.objects.create(name=currency.name, abbreviation=ticker, type_currency='CURRENCY')
                print(ticker, '--CREATED')
            except:
                print(ticker, '--ALREADY EXIST')


if __name__ == '__main__':
    load_currencies()
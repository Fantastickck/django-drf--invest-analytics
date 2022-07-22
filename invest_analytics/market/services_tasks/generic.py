from decimal import Decimal

from tinkoff.invest import Client


def get_figi(client: Client, ticker: str, type_instrument: str):
    search_instruments = client.instruments.find_instrument(query=ticker).instruments
    for instrument in reversed(search_instruments):
        if all([instrument.instrument_type == type_instrument, ticker == instrument.ticker]):
            return instrument.figi


def get_decimal_price(obj, lot) -> Decimal:
    price = obj.last_prices[0].price
    units = str(price.units)
    nano = str(price.nano)
    if lot == 10000:
        decimal_price = Decimal(f'{units}.0{nano}') 
    elif lot == 100000 or lot == 1000000:
        decimal_price = Decimal(f'{units}.00{nano}') 
    else:
        decimal_price = Decimal(f'{units}.{nano}')
    return decimal_price
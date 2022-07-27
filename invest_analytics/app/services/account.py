from decimal import Decimal


def get_result_currency_position(obj, obj_attr, currency_to, currency_courses):
    if obj.asset.currency == currency_to:
        return obj_attr
    currency_from = obj.asset.currency
    course = currency_courses[currency_from]
    return Decimal(obj_attr * course)


def get_total_invested(obj, currency):
    asset_invested = sum(
        position.get_invested(currency) for position in obj.positions.all()
    )
    # currency_invested = sum(
    #     position.get(currency) for position in obj.currency_positions.all()
    # )
    return Decimal(asset_invested).quantize(Decimal('0.00'))


def get_total_amount(obj, currency, courses):
    asset_amount = sum(
        position.get_current_amount(currency, courses)*position.quantity
        for position in obj.positions.all()
    )
    # currency_amount = sum(
    #     position.get_currenct_amount(currency) for position in obj.currency_positions.all()
    # )
    return Decimal(asset_amount).quantize(Decimal('0.00'))


def get_total_profit(data):
    total_profit = 0
    for position in data['positions']:
        total_profit += position['profit']
    return total_profit


def get_total_profit_percent(data):
    total_invested = data['total_invested']
    total_amount = data['total_amount']
    try:
        result = Decimal(100 * (total_amount - total_invested)/total_invested).quantize(Decimal('0.00'))
    except:
        result = 0
    return result

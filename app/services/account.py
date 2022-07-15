from decimal import Decimal


def get_result_currency_position(obj, obj_attr, currency_to, currency_courses):
    if obj.asset.currency == currency_to:
        return obj_attr
    currency_from = obj.asset.currency
    course = currency_courses[currency_from]
    return Decimal(obj_attr * course)


def get_total_amount(data):
    total_amount = 0
    for position in data['positions']:
        total_amount += position['current_amount']
    return total_amount


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

from decimal import Decimal

from django.contrib import admin

from .models import (
    Account,
    # AccountHistoricalModel,
    Position,
    Operation
)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'total_invested_usd', 'total_invested_rub')
    list_display_links = ('id', 'name')

    @admin.display(description='Инвестировано USD')
    def total_invested_usd(self, obj):
        return Decimal(sum([position.avg_price_usd*position.quantity for position in obj.positions.all()]))\
            .quantize(Decimal('0.00'))
    
    @admin.display(description='Инвестировано RUB')
    def total_invested_rub(self, obj):
        return Decimal(sum([position.avg_price_rub*position.quantity for position in obj.positions.all()]))\
            .quantize(Decimal('0.00'))


# @admin.register(AccountHistoricalModel)
# class StatesAdmin(admin.ModelAdmin):
#     list_display = ('account', 
#         'date', 'total_amount_rounded', 'total_profit_rounded')

#     @admin.display(description='Стоимость')
#     def total_amount_rounded(self, obj):
#         return obj.total_amount.quantize(Decimal('0.00'))

#     @admin.display(description='Прибыль')
#     def total_profit_rounded(self, obj):
#         return obj.total_profit.quantize(Decimal('0.00'))


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'asset', 
        'avg_price_usd_rounded', 
        'avg_price_rub_rounded', 
        'quantity', 
        'account')
    # list_display_links = ()

    @admin.display(description='Средняя цена USD')
    def avg_price_usd_rounded(self, obj):
        return obj.avg_price_usd.quantize(Decimal('0.00'))

    @admin.display(description='Средняя цена RUB')
    def avg_price_rub_rounded(self, obj):
        return obj.avg_price_rub.quantize(Decimal('0.00'))


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('date', 'asset', 'account', 'price', 
    'quantity', 'commission', 'currency', 'type_operation')
    # list_display_links = ()

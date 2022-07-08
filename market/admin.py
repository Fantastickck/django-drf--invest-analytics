from decimal import Decimal

from django.contrib import admin

from .models import (
    Asset,
    Currency,
    TypeAsset,
    Sector,
    Country,
    Market
)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'type_asset',
        'currency', 'sector', 'country', 'market', 'last_price_quantize')
    list_display_links = ('ticker',)

    @admin.display()
    def last_price_quantize(self, obj):
        return obj.last_price.quantize(Decimal('2.00'))

    last_price_quantize.short_description = 'Текущая цена'


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name', 'symbol')
    list_display_links = ('abbreviation',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_alpha_2', 'iso_alpha_3', 'iso_number')
    list_display_links = ('name',)


admin.site.register(TypeAsset)
admin.site.register(Sector)
admin.site.register(Market)

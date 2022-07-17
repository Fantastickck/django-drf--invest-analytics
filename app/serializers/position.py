from decimal import Decimal
from rest_framework import serializers

from app.models.position import Position
from market.models.asset import Asset

from app.services.account import get_result_currency_position


class AssetPositionSerializer(serializers.ModelSerializer):
    """Asset model serializer for field in PositionSerializer"""
    type_asset = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    currency = serializers.SlugRelatedField(
        slug_field='abbreviation', read_only=True)
    sector = serializers.SlugRelatedField(slug_field='name', read_only=True)
    country = serializers.SlugRelatedField(
        slug_field='iso_alpha_3', read_only=True)

    class Meta:
        model = Asset
        fields = ('id', 'name', 'ticker', 'last_price', 'type_asset',
                  'currency', 'sector', 'country', 'last_price')


class PositionSerializer(serializers.ModelSerializer):
    asset = AssetPositionSerializer()
    avg_price = serializers.SerializerMethodField('get_avg_price')
    profit = serializers.SerializerMethodField('get_profit')
    profit_percent = serializers.SerializerMethodField('get_profit_percent')
    invested = serializers.SerializerMethodField('get_invested')
    current_amount = serializers.SerializerMethodField('get_current_amount')

    class Meta:
        model = Position
        fields = ('id', 'asset', 'avg_price', 'profit', 'profit_percent', 'invested', 'current_amount', 'quantity')

    def get_avg_price(self, position):
        if self.context.get('currency').abbreviation == 'USD':
            avg_price = position.avg_price_usd
        else:
            avg_price = position.avg_price_rub
        self.context['last_price'] = get_result_currency_position(
            position,
            position.asset.last_price,
            self.context.get('currency'),
            self.context.get('currency_courses')
        )
        self.context['avg_price'] = avg_price
        return avg_price

    def get_invested(self, position):
        invested = Decimal(self.context['avg_price'] * position.quantity)
        return invested

    def get_current_amount(self, position):
        current_amount = Decimal(
            self.context['last_price'] * position.quantity).quantize(Decimal('0.00'))
        return current_amount

    def get_profit(self, position):
        profit = Decimal((self.context['last_price'] - self.context['avg_price']) 
        * position.quantity).quantize(Decimal('0.00'))
        return profit

    def get_profit_percent(self, position):
        return Decimal(100 * (self.context['last_price'] - self.context['avg_price']) 
        / self.context['avg_price']).quantize(Decimal('0.00'))

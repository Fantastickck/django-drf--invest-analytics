from decimal import Decimal
from rest_framework import serializers

from app.models.position import Position
from market.models.asset import Asset

from app.services.account import get_result_currency_position


class AssetPositionSerializer(serializers.ModelSerializer):
    type_asset = serializers.SlugRelatedField(slug_field='name', read_only=True)
    currency = serializers.SlugRelatedField(slug_field='abbreviation', read_only=True)
    sector = serializers.SlugRelatedField(slug_field='name', read_only=True)
    country = serializers.SlugRelatedField(slug_field='iso_alpha_3', read_only=True)

    class Meta:
        model = Asset
        fields = ('id', 'name', 'ticker', 'last_price', 'type_asset', 'currency', 'sector', 'country', 'last_price')


class PositionSerializer(serializers.ModelSerializer):
    asset = AssetPositionSerializer()
    avg_price = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField(source='get_profit')
    profit_percent = serializers.SerializerMethodField(source='get_profit_percent')
    invested = serializers.SerializerMethodField(source='get_invested')
    current_amount = serializers.SerializerMethodField('get_current_amount')

    class Meta:
        model = Position
        fields = '__all__'

    def get_avg_price(self, position):
        avg_price = position.avg_price
        result_in_currency = get_result_currency_position(
            position, 
            avg_price, 
            self.context.get('currency'), 
            self.context.get('currency_courses'))
        return result_in_currency

    def get_invested(self, position):
        invested = Decimal(position.avg_price * position.quantity)
        result_in_currency = get_result_currency_position(
            position, 
            invested, 
            self.context.get('currency'), 
            self.context.get('currency_courses'))
        return result_in_currency

    def get_current_amount(self, position):
        current_amount = Decimal(position.asset.last_price * position.quantity)
        result_in_currency = get_result_currency_position(
            position, 
            current_amount, 
            self.context.get('currency'), 
            self.context.get('currency_courses'))
        return result_in_currency

    def get_profit(self, position):
        profit = Decimal((position.asset.last_price - position.avg_price) * position.quantity).quantize(Decimal('0.00'))
        result_in_currency = get_result_currency_position(
            position, 
            profit, 
            self.context.get('currency'), 
            self.context.get('currency_courses'))
        return result_in_currency
    
    def get_profit_percent(self, position):
        return Decimal((position.asset.last_price - position.avg_price) / position.avg_price).quantize(Decimal('0.00'))

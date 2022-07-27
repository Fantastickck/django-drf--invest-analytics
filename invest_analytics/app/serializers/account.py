from decimal import Decimal

from rest_framework import serializers

from app.models.account import Account
from app.models.position import Position

from app.serializers.position import PositionSerializer


class AccountListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


class AccountDetailSerializer(serializers.ModelSerializer):
    """
    Account model serializer with all data 
    and counting about financial results.
    """

    calculated_currency = serializers.SerializerMethodField()
    total_invested = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    total_profit = serializers.SerializerMethodField()
    total_profit_percent = serializers.SerializerMethodField()
    positions = serializers.SerializerMethodField('get_positions_serializer')

    class Meta:
        model = Account
        fields = (
            'id',
            'name', 
            'user', 
            'calculated_currency',
            'total_invested',
            'total_amount',
            'total_profit',
            'total_profit_percent',
            'positions'
        )

    def get_calculated_currency(self, account):
        return self.context.get('currency').abbreviation

    def get_total_invested(self, account):
        return self.context.get('total_invested')

    def get_total_amount(self, account):
        return self.context.get('total_amount')
    
    def get_total_profit(self, account):
        return self.context.get('total_amount') \
            - self.context.get('total_invested')

    def get_total_profit_percent(self, account):
        total_amount = self.context.get('total_amount')
        total_invested = self.context.get('total_invested')
        try:
            return Decimal(100 * ((total_amount) - total_invested) \
                    / total_invested).quantize(Decimal('0.00'))
        except:
            return 0
        
    def get_positions_serializer(self, account):
        """
        Create positions field with PositionSerializer 
        and data about currencies,
        pass data from this serializer to context.
        """
        serializer_context = {
            'currency': self.context.get('currency'),
            'currency_courses': self.context.get('currency_courses'),
            'total_amount': self.context.get('total_amount'),
        }
        positions = Position.objects.filter(account=account).prefetch_related(
            'asset',
            'asset__sector', 
            'asset__currency',
            'asset__type_asset', 
            'asset__country',
        )
        serializer = PositionSerializer(positions, many=True, context=serializer_context)
        return serializer.data

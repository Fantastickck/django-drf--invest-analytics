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

    positions = serializers.SerializerMethodField('get_positions_serializer')
    total_invested = serializers.SerializerMethodField('get_total_invested')
    total_profit = serializers.DecimalField(
        max_digits=20, decimal_places=6, required=False)
    calculated_currency = serializers.SerializerMethodField('get_calc_currency')

    class Meta:
        model = Account
        fields = '__all__'

    def get_total_invested(self, account):
        total_invested = sum([position['invested'] for position in self.context['position_data']])
        return total_invested
        
    def get_calc_currency(self, account):
        return self.context.get('currency').abbreviation
        
    def get_positions_serializer(self, account):
        """
        Create positions field with PositionSerializer 
        and data about currencies,
        pass data from this serializer to context.
        """
        serializer_context = {
            'currency': self.context.get('currency'),
            'currency_courses': self.context.get('currency_courses')
        }
        positions = Position.objects.filter(account=account).prefetch_related(
            'asset',
            'asset__sector', 
            'asset__currency',
            'asset__type_asset', 
            'asset__country',
        )
        serializer = PositionSerializer(positions, many=True, context=serializer_context)
        self.context['position_data'] = serializer.data
        return serializer.data

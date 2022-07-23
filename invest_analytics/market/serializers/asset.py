from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from market.models.asset import Asset
from market.models.currency import Currency
from market.models.asset_specs import (
    TypeAsset,
    Country,
    Sector,
    Market
)



class AssetListSerializer(serializers.ModelSerializer):
    type_asset = serializers.CharField(source='type_asset.name')
    currency = serializers.CharField(source='currency.abbreviation')
    sector = serializers.CharField(source='sector.name')
    country = serializers.CharField(source='country.iso_alpha_3')
    market = serializers.CharField(source='market.name')

    class Meta:
        model = Asset
        fields = ('id', 'name', 'ticker', 'type_asset', 'currency',
                  'sector', 'country', 'market', 'last_price')

    def create(self, validated_data):
        asset = Asset.objects.create(
            name=validated_data['name'],
            ticker=validated_data['ticker'],
            type_asset = TypeAsset.objects.filter(
                name=validated_data['type_asset']['name'])[0],
            currency = Currency.objects.filter(
                abbreviation=validated_data['currency']['abbreviation'])[0],
            sector = Sector.objects.filter(
                name=validated_data['sector']['name'])[0],
            country = Country.objects.filter(
                iso_alpha_3=validated_data['country']['iso_alpha_3'])[0],
            market = Market.objects.filter(name=validated_data['market']['name'])[0],
            last_price = validated_data['last_price']
        )
        return asset


class AssetDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = '__all__'
        depth = 1

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from market.models.asset import Asset
from market.models.currency import Currency
from market.models.asset_specs import (
    TypeAsset,
    Sector,
    Country,
    Market
)


class AssetTests(APITestCase):

    def setUp(self):
        self.type_asset = TypeAsset.objects.create(name='Stock')
        self.sector = Sector.objects.create(name='IT')
        self.country = Country.objects.create(
            name='США', iso_alpha_2='US', iso_alpha_3='USA', iso_number=840
        )
        self.market_nasdaq = Market.objects.create(name='NASDAQ')
        self.market_nyse = Market.objects.create(name='NYSE')
        self.currency = Currency.objects.create(
            name='Доллар США', 
            type_currency='CURRENCY', 
            abbreviation='USD', 
            symbol='$'
        )
        self.asset_apple = Asset.objects.create(
            name='Apple',
            ticker='AAPL',
            type_asset = self.type_asset,
            currency = self.currency,
            sector = self.sector,
            country = self.country,
            market = self.market_nyse,
            last_price = 120
        )
        self.asset_abbot = Asset.objects.create(
            name='Abbott',
            ticker='ABT',
            type_asset = self.type_asset,
            currency = self.currency,
            sector = self.sector,
            country = self.country,
            market = self.market_nyse,
            last_price = 100
        )

    def test_get_asset_list(self):
        response = self.client.get(reverse('asset_list'))
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 2)
    
    def test_get_asset_detail_status_codes(self):
        response_1 = self.client.get(
            reverse('asset_detail', kwargs={'pk': self.asset_apple.pk})
        )
        response_2 = self.client.get(
            reverse('asset_detail', kwargs={'pk': 0})
        )
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_asset(self):
        payload = {
            'name': 'Microsoft',
            'ticker': 'MSFT',
            'type_asset': 'Stock',
            'currency': 'USD',
            'sector': 'IT',
            'country': 'USA',
            'market': 'NASDAQ',
            'last_price': 300
        }
        response = self.client.post('/market/assets/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
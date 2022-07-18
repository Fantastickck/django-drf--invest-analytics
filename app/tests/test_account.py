from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from app.models.account import Account
from app.models.position import Position
from market.models.asset import Asset
from market.models.asset_specs import Country, Market, Sector, TypeAsset
from market.models.currency import Currency, CurrencyCourse

from app.serializers.position import AssetPositionSerializer


class AccountTests(APITestCase):

    def setUp(self):
    
        self.user = User.objects.create(username='TestUser', password='testPassword')
        self.account_1 = Account.objects.create(user=self.user, name='Test_1')
        self.account_2 = Account.objects.create(user=self.user, name='Test_2')
        self.currency_usd = Currency.objects.create(
            name='Американский доллар', 
            type_currency='CURRENCY', 
            abbreviation='USD', 
            symbol='$')
        self.currency_rub = Currency.objects.create(
            name='Российский рубль', 
            type_currency='CURRENCY', 
            abbreviation='RUB', 
            symbol='#')
        CurrencyCourse.objects.create(currency_from=self.currency_usd, currency_to=self.currency_rub, value=60)
        CurrencyCourse.objects.create(currency_from=self.currency_rub, currency_to=self.currency_usd, value=0.016667)
        type_asset = TypeAsset.objects.create(name='Stock')
        sector_it = Sector.objects.create(name='Информационные технологии')
        sector_fin = Sector.objects.create(name='Финансы')
        country = Country.objects.create(name='США', iso_alpha_2='US', iso_alpha_3='USA', iso_number=840)
        market = Market.objects.create(name='NASDAQ')
        asset_1 = Asset.objects.create(
            name='Apple', 
            ticker='AAPL', 
            currency=self.currency_usd, 
            type_asset=type_asset, 
            sector=sector_it, 
            country=country, 
            market=market,
            last_price=160
        )
        asset_2 = Asset.objects.create(
            name='Сбербанк', 
            ticker='SBER', 
            currency=self.currency_rub, 
            type_asset=type_asset, 
            sector=sector_fin, 
            country=country, 
            market=market,
            last_price=140
        )
        # USD/RUB = 55
        self.position_1 = Position.objects.create(
            account=self.account_2,
            asset=asset_1,
            avg_price_usd=150,
            avg_price_rub=8250,
            quantity=3,
        )
        # USD/RUB = 50
        self.position_2 = Position.objects.create(
            account=self.account_2,
            asset=asset_2,
            avg_price_usd=2.52,
            avg_price_rub=126,
            quantity=110,
        )
            

    def test_get_accounts_list(self):
        response = self.client.get(reverse('list_accounts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_detail_status_codes(self):
        """Account without positions."""
        response_1 = self.client.get(reverse('detail_account', kwargs={'pk': self.account_1.pk}))
        """Account with positions."""
        response_2 = self.client.get(reverse('detail_account', kwargs={'pk': self.account_2.pk}))
        """Account does not exist."""
        response_3 = self.client.get(reverse('detail_account', kwargs={'pk': 0}))
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_3.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_account(self):
        data = {
            'name': 'account_3',
            'user': self.user.pk
        }
        response = self.client.post('/api/v1/accounts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_account_detail_data(self):
        """With course of USD/RUB = 60"""
        response_rub = self.client.get(f'/api/v1/accounts/{self.account_2.pk}/?currency=RUB')
        response_usd = self.client.get(f'/api/v1/accounts/{self.account_2.pk}/?currency=USD')
        data_rub = response_rub.json()
        data_usd = response_usd.json()
        expected_data_rub = {
            "id": self.account_2.pk,
            "positions": [
                {
                    "id": self.position_1.pk,
                    "asset": AssetPositionSerializer(self.position_1.asset).data,
                    "avg_price": 8250.0,
                    "profit": 4050.0,
                    "profit_percent": 16.36,
                    "invested": 24750.0,
                    "current_amount": 28800.0,
                    "quantity": 3
                },
                {
                    "id": self.position_2.pk,
                    "asset": AssetPositionSerializer(self.position_2.asset).data,
                    "avg_price": 126.0,
                    "profit": 1540.0,
                    "profit_percent": 11.11,
                    "invested": 13860.0,
                    "current_amount": 15400.0,
                    "quantity": 110,
                }
            ],
            "total_invested": 38610.0,
            "calculated_currency": "RUB",
            "name": "Test_2",
            "user": self.user.pk,
            "total_amount": 44200.0,
            "total_profit": 5590.0,
            "total_profit_percent": 14.48
        }
        expected_data_usd = {
            "id": self.account_2.pk,
            "positions": [
                {
                    "id": self.position_1.pk,
                    "asset": AssetPositionSerializer(self.position_1.asset).data,
                    "avg_price": 150.0,
                    "profit": 30.0,
                    "profit_percent": 6.67,
                    "invested": 450.0,
                    "current_amount": 480.0,
                    "quantity": 3
                },
                {
                    "id": self.position_2.pk,
                    "asset": AssetPositionSerializer(self.position_2.asset).data,
                    "avg_price": 2.52,
                    "profit": -20.53,
                    "profit_percent": -7.41,
                    "invested": 277.2,
                    "current_amount": 256.67,
                    "quantity": 110,
                }
            ],
            "total_invested": 727.2,
            "calculated_currency": "USD",
            "name": "Test_2",
            "user": self.user.pk,
            "total_amount": 736.67,
            "total_profit": 9.47,
            "total_profit_percent": 1.3
        }
        self.assertEqual(data_rub, expected_data_rub)
        self.assertEqual(data_usd, expected_data_usd)

    def test_get_account_detail_wrong_currency(self):
        response = self.client.get('/api/v1/accounts/1/?currency=_')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_account_wrong_user_pk(self):
        data = {
            'name': 'account_3',
            'user': 0
        }
        response = self.client.post('/api/v1/accounts/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

from app.models.account import Account
from market.models.currency import Currency, CurrencyCourse


class AccountTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='testPassword')
        self.account = Account.objects.create(user=self.user, name='Test')
        self.currency_usd = Currency.objects.create(name='Американский доллар', abbreviation='USD', symbol='$')
        self.currency_rub = Currency.objects.create(name='Российский рубль', abbreviation='RUB', symbol='#')
        CurrencyCourse.objects.create(currency_from=self.currency_usd, currency_to=self.currency_rub, value=60)
        CurrencyCourse.objects.create(currency_from=self.currency_rub, currency_to=self.currency_usd, value=0.0167)

    def test_get_accounts_list(self):
        response = self.client.get(reverse('list_accounts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_detail(self):
        response = self.client.get(reverse('detail_account', kwargs={'pk': self.account.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_get_account_detail(self):
        response = self.client.get(reverse('detail_account', kwargs={'pk': 0}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from rest_framework.test import APITestCase

from market.models.currency import (
    Currency,
    CurrencyCourse
)

from market.load_data import load_currencies
from market.tasks import update_currency_courses

class CurrencyCoursesTest(APITestCase):

    def test_create_currencies(self):
        load_currencies()
        self.assertTrue(
            Currency.objects.filter(abbreviation__in=['USD', 'RUB']).exists())
        self.assertTrue(Currency.objects.all().count(), 17)
        
    def test_update_currency_courses(self):
        load_currencies()
        update_currency_courses()
        self.assertTrue(CurrencyCourse.objects.all().exists())
        self.assertTrue(CurrencyCourse.objects.all().count(), 36)
        
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response

from app.serializers.account import AccountListSerializer, AccountDetailSerializer

from app.models.account import Account
from market.models.currency import Currency

from app.services.account import (
    get_total_amount,
    get_total_profit,
    get_total_profit_percent
)


class AccountListView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer


class AccountDetailView(views.APIView):
    def get(self, request, pk):
        calc_currency = request.GET.get('currency', 'RUB').upper()
        currency_to = get_object_or_404(Currency, abbreviation=calc_currency)
        currency_courses = {}
        for course in currency_to.currencies_to.all():
            currency_courses[course.currency_from] = course.value
        account = get_object_or_404(Account.objects.select_related('user').prefetch_related(
            'positions', 'operations'
        ), pk=pk)
        data = AccountDetailSerializer(account, context={
            'currency': currency_to,
            'currency_courses': currency_courses
        }).data
        data['total_amount'] = get_total_amount(data)
        data['total_profit'] = get_total_profit(data)
        data['total_profit_percent'] = get_total_profit_percent(data)
        return Response(data)

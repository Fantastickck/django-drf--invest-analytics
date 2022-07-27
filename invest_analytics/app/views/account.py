from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.response import Response

from app.serializers.account import AccountListSerializer, AccountDetailSerializer

from app.models.account import Account
from market.models.currency import Currency

from app.services.account import (
    get_total_amount,
    get_total_invested,
)


class AccountListView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer


class AccountDetailView(views.APIView):
    def get(self, request, pk):
        calc_currency_abbr = request.GET.get('currency').upper()
        if calc_currency_abbr not in ('RUB', 'USD'):
            return Response(
                {'detail': 'Wrong currency'},
                status=status.HTTP_404_NOT_FOUND
            )
        calc_currency = get_object_or_404(
            Currency.objects
            .prefetch_related('currencies_to__currency_from'),
            abbreviation=calc_currency_abbr
        )
        currency_courses = {}
        for course in calc_currency.currencies_to.all():
            currency_courses[course.currency_from] = course.value
        account = get_object_or_404(
            Account.objects
            .select_related('user')
            .prefetch_related(
                'positions',  
                'positions__asset__currency'            
            ),
            pk=pk
        )
        total_invested = get_total_invested(account, calc_currency)
        total_amount = get_total_amount(account, calc_currency, currency_courses)
        serializer = AccountDetailSerializer(account, context={
            'currency': calc_currency,
            'currency_courses': currency_courses,
            'total_invested': total_invested,
            'total_amount': total_amount
        })
        return Response(serializer.data)

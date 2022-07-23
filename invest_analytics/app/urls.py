from django.urls import path, include

from app.views.account import (
    AccountDetailView, 
    AccountListView
)


urlpatterns = [
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),

    path(r'accounts/', AccountListView.as_view(), name='account_list'),
    path(r'accounts/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
]
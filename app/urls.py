from django.urls import path, include

from .views.account import (
    AccountDetailView, 
    AccountListView
)


urlpatterns = [
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),

    path(r'accounts/', AccountListView.as_view(), name='list_accounts'),
    path(r'accounts/<int:pk>/', AccountDetailView.as_view(), name='detail_account'),
]
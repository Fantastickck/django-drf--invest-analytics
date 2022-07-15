from django.urls import path, include

from .views.account import (
    AccountDetailView, 
    AccountListView
)


urlpatterns = [
    path(r'auth/', include('djoser.urls'), name='list_accounts'),
    path(r'auth/', include('djoser.urls.authtoken'), name='detail_account'),

    path(r'accounts/', AccountListView.as_view()),
    path(r'accounts/<int:pk>/', AccountDetailView.as_view()),
]
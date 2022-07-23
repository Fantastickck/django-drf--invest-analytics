from django.urls import path

from market.views.asset import (
    AssetListView,
    AssetDetailView
)


urlpatterns = [
    path(r'assets/', AssetListView.as_view(), name='asset_list'),
    path(r'assets/<int:pk>/', AssetDetailView.as_view(), name='asset_detail')
]
from rest_framework import generics

from market.models.asset import Asset

from market.serializers.asset import (
    AssetDetailSerializer, 
    AssetListSerializer
)


class AssetListView(generics.ListCreateAPIView):
    serializer_class = AssetListSerializer

    def get_queryset(self):
        queryset = Asset.objects.all().select_related(
            'type_asset',
            'currency',
            'sector',
            'country',
            'market'
        )
        return queryset


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetDetailSerializer
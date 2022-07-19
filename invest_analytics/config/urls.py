from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/v1/', include('app.urls')),
    path(r'market/', include('market.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

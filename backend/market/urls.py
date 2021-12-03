from django.urls import path
from .views import Market, MarketWarehouse

urlpatterns = [
    path('', MarketWarehouse.as_view()),
    path('createorder/', Market.as_view())
]

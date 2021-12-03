from django.urls import path
from .views import SelfDeliveryMapMarkers, PartnersMapViewer

urlpatterns = [
    path('delivery/', SelfDeliveryMapMarkers.as_view()),
    path('partners/', PartnersMapViewer.as_view()),
]

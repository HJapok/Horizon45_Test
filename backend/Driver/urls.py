from django.urls import path
from .views import *


urlpatterns = [
    path('truck/', TruckView.as_view(),name='retrieve-truck'),
    path('truck/<int:pk>/', TruckView.as_view(),name='retrieve-truck-details'),
    path('driver/', DriverView.as_view(),name='retrieve-driver'),
    path('driver/<int:pk>/', DriverView.as_view(),name='retrieve-driver-details'),
    path('driver/email=<str:email>/', DriverView.as_view(),name='retrieve-driver-details-by-email'),
    path('driver/mobile_number=<str:mobile_number>/', DriverView.as_view(),name='retrieve-driver-details-by-mobile_number'),
    path('driver/plate_number=<str:plate_number>/', DriverView.as_view(),name='retrieve-driver-details-by-plate_number'),
    path('driver/language=<str:language>/', DriverView.as_view(),name='retrieve-driver-details-by-language'),
]
from django.urls import path
from restaurant.views import (
    ListCreateRestaurantsApi,
    RetrieveRestaurantApi,
)
app_name = 'restaurant'

urlpatterns = [
    path('', ListCreateRestaurantsApi.as_view(), name='list'),
    path('<int:id>', RetrieveRestaurantApi.as_view(), name='retrieve'),
]

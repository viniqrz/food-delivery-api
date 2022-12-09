from django.urls import path
from restaurant.views import (
    ListRestaurantsApi,
    RetrieveRestaurantApi,
)
app_name = 'restaurant'

urlpatterns = [
    path('', ListRestaurantsApi.as_view(), name='list'),
    path('<int:id>', RetrieveRestaurantApi.as_view(), name='retrieve'),
]

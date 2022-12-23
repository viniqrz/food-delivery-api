from django.urls import path
from restaurant.views import (
    ListCreateRestaurantsApi,
    RetrieveRestaurantApi,
)
from order.views import ListMyRestaurantOrdersApi, AcceptOrderApi
app_name = 'restaurant'

urlpatterns = [
    path('', ListCreateRestaurantsApi.as_view(), name='list'),
    path('<int:id>', RetrieveRestaurantApi.as_view(), name='retrieve'),
    path('<int:id>/orders', ListMyRestaurantOrdersApi.as_view(), name='my-orders'),
    path('<int:restaurant_id>/orders/<int:order_id>/accept',
         AcceptOrderApi.as_view(), name='accept-order')
]

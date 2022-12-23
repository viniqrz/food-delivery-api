from django.urls import path
from order.views import (
    ListMyOrdersApi,
    CreateOrderApi,
    ListAvailableForDeliveryOrdersApi
)
app_name = 'order'

urlpatterns = [
    path('/my-orders', ListMyOrdersApi.as_view(), name='list'),
    path('', CreateOrderApi.as_view(), name='create'),
    path('/available-for-delivery',
         ListAvailableForDeliveryOrdersApi.as_view(), name='list-available')
]

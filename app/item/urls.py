from rest_framework import routers
from django.urls import include, path
from item.views import ReadItemViewSet, CreateItemApi

router = routers.DefaultRouter()

router.register(r'item', ReadItemViewSet)

app_name = 'item'

urlpatterns = [
    path('', include(router.urls), name='read-item'),
    path('item', CreateItemApi.as_view(), name='create-item')
]
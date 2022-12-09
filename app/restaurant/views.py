from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    mixins,
)
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from core.models import Restaurant
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from user.views  import UserSerializer


class RestaurantSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Restaurant
        fields = ['name', 'cnpj', 'description', 'user']
        read_only_fields = ['user']
        


class RestaurantsPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'offset'
    max_page_size = 50


class ListRestaurantsApi(ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    pagination_class = RestaurantsPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveRestaurantApi(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'

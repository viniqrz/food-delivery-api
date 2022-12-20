from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    PrimaryKeyRelatedField
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from restaurant.views import RestaurantSerializer
from core.models import Item, Restaurant
from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication


class ReadItemSerializer(ModelSerializer):
    restaurant = StringRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'restaurant']
        read_only_fields = ['id']


class ItemsPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'offset'
    max_page_size = 50


class ReadItemViewSet(ReadOnlyModelViewSet):
    serializer_class = ReadItemSerializer
    queryset = Item.objects.all()
    pagination_class = ItemsPagination


class CreateItemSerializer(ModelSerializer):
    restaurant = PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'restaurant']
        read_only_fields = ['id']


class CreateItemApi(APIView):
    serializer_class = CreateItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = CreateItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            restaurant_id = serializer.validated_data.get('restaurant').id
            Restaurant.objects.get(user=self.request.user,
                                   pk=restaurant_id)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Restaurant.DoesNotExist:
            return Response({'message': 'Not owner'}, status=status.HTTP_400_BAD_REQUEST)

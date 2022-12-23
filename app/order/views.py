from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, DecimalField
from rest_framework.permissions import IsAuthenticated
from core.models import Order, Item, Restaurant
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class OrdersPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'offset'
    max_page_size = 50


class ItemDetailSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'restaurant']
        read_only_fields = ['id']


class RestaurantDetailSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'cnpj', 'description', 'user']
        read_only_fields = ['user', 'id']


class ListOrderSerializer(ModelSerializer):
    items = ItemDetailSerializer(many=True)
    restaurant = RestaurantDetailSerializer()

    class Meta:
        model = Order

        fields = ['customer', 'note', 'items', 'restaurant',
                  'status', 'delivery_method', 'delivery_worker', 'created_at', 'delivered_at', 'updated_at']
        read_only_fields = ['customer', 'status',
                            'delivery_method', 'delivery_worker']


class ListMyOrdersApi(ListAPIView):
    serializer_class = ListOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    pagination_class = OrdersPagination

    def get_queryset(self):
        return self.queryset.filter(customer=self.request.user)


class ListAvailableForDeliveryOrdersApi(ListAPIView):
    serializer_class = ListOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    pagination_class = OrdersPagination

    def get(self, request, *args, **kwargs):
        if (request.user.is_delivery_worker):
            return super().get(request, *args, **kwargs)
        else:
            return Response(
                {'message': 'You are not a worker'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        return self.queryset.filter(status=Order.StatusEnum.PRODUCTION)


class ListMyRestaurantOrdersApi(ListAPIView):
    serializer_class = ListOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    pagination_class = OrdersPagination

    def get_queryset(self):
        return self.queryset.filter(
            restaurant=Restaurant.objects.get(pk=self.kwargs['id'])
        )


class CreateOrderSerializer(ModelSerializer):
    items = PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())
    restaurant = PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Order
        fields = ['customer', 'note', 'items', 'restaurant', 'status']
        read_only_fields = ['customer', 'status']


class CreateOrderApi(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class AcceptOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class AcceptOrderApi(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'order_id'

    def patch(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(
            pk=kwargs.get('restaurant_id'), user=self.request.user)
            order_id = kwargs.get('order_id')

            Order.objects.filter(restaurant=restaurant, pk=order_id).update(
                status=Order.StatusEnum.PRODUCTION
            )
            return Response({'message': 'Accepted'}, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({'message': 'Not owner'}, status=status.HTTP_403_FORBIDDEN)

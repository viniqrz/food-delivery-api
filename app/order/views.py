from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from rest_framework.permissions import IsAuthenticated
from core.models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class OrdersPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'offset'
    max_page_size = 50

class ListOrderSerializer(ModelSerializer):
    class Meta:
        model: Order
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


class CreateOrderApi(APIView):
    permission_classes = [IsAuthenticated]

    class CreateOrderSerializer(ModelSerializer):
        items = PrimaryKeyRelatedField(many=True)
        restaurant = PrimaryKeyRelatedField()

        class Meta:
            model: Order
            fields = ['customer', 'note', 'items', 'restaurant', 'status']
            read_only_fields = ['customer', 'status']

    def post(self, request, response, **kwargs):
        serializer = self.CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

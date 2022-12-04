from rest_framework.generics import GenericAPIView
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import User

class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['is_active', 'email', 'first_name', 'last_name', 'password']
        read_only_fields=['is_active']  

    def create(self, validated_data):
        """Create and return an user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

class CreateUserApi(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

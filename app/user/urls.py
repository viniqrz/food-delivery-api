from django.urls import path
from user.views import CreateUserApi

app_name = 'user'

urlpatterns = [
    path('', CreateUserApi.as_view(), name='create'),
]
from django.db import models
from core.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=80)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.name
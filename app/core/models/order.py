from django.db.models import (
    Model,
    ForeignKey,
    ManyToManyField,
    DateTimeField,
    TextChoices,
    CASCADE,
    CharField,
    TextField
)
from core.models import Item, Restaurant, User


class Order(Model):

    class DeliveryMethodEnum(TextChoices):
        RESTAURANT = 'Restaurant'
        APP = 'App'

    class StatusEnum(TextChoices):
        PENDING = 'Pending'
        PRODUCTION = 'Production'
        SENT = 'Sent'
        DELIVERED = 'Delivered'

    note = TextField(default='')
    customer = ForeignKey(to=User, on_delete=CASCADE, related_name='customer')
    items = ManyToManyField(to=Item)
    restaurant = ForeignKey(to=Restaurant, on_delete=CASCADE)
    status = CharField(choices=StatusEnum.choices,
                       default=StatusEnum.PENDING, max_length=64)
    delivery_method = CharField(
        choices=DeliveryMethodEnum.choices, max_length=64)
    devivery_worker = ForeignKey(
        to=User, null=True, on_delete=CASCADE, related_name='worker')
    created_at = DateTimeField(auto_now_add=True)
    delivered_at = DateTimeField(null=True)
    updated_at = DateTimeField(auto_now=True)

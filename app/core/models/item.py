from django.db.models import (
    Model,
    CharField,
    TextField,
    ForeignKey,
    DecimalField,
    CASCADE
)
from core.models import Restaurant


class Item(Model):
    name = CharField(max_length=255)
    description = TextField()
    price = DecimalField(max_digits=6, decimal_places=2)
    restaurant = ForeignKey(to=Restaurant, on_delete=CASCADE)

    def __str__(self):
        return self.name
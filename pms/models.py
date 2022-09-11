from datetime import date

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(default=date.today())
    stock = models.IntegerField(default=1)
    status = models.BooleanField(default=True)

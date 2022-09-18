from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models


class Drug(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    stock = models.IntegerField(default=1)
    expiry_date = models.DateField()
    price = models.IntegerField(default=1)

    def is_expired(self):
        return timezone.now().date() > self.expiry_date

    def __str__(self):
        return f'{self.id} {self.name}'


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=False)
    drugs = models.ManyToManyField(Drug)
    quantity = models.IntegerField()

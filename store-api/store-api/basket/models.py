from django.db import models
from clients.models import Clients
from products.models import Products


class BasketProducts(models.Model):
    """
    This model contains products that client adds to basket
    """
    client = models.ForeignKey(Clients, verbose_name='Client', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Product', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Basket product'
        verbose_name_plural = 'Basket products'

from django.db import models
from .settings import OrdersStatuses
from clients.models import Clients
from products.models import Products


class Orders(models.Model):
    """
    This model contains all orders created by clients
    """
    client = models.ForeignKey(Clients, verbose_name='Client', on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    status = models.CharField(verbose_name='Status', max_length=255,
                              choices=OrdersStatuses.choices(), default=OrdersStatuses.WAITING_FOR_PAYMENT.value)

    def __str__(self):
        return f'Order of {self.client.__str__()}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderProducts(models.Model):
    """
    This model contains products that clients adds to orders
    """
    order = models.ForeignKey(Orders, verbose_name='Order product', on_delete=models.PROTECT)
    product = models.ForeignKey(Products, verbose_name='Product', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product} of order {self.order}'

    class Meta:
        verbose_name = 'Order product'
        verbose_name_plural = 'Order products'


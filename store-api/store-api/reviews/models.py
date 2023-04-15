from django.db import models
from clients.models import Clients
from products.models import Products
from django.core.validators import MaxValueValidator, MinValueValidator


class Reviews(models.Model):
    """
    This model contains records of products reviews
    Client must place an order with the product before leaving review
    """
    product = models.ForeignKey(Products, verbose_name='Product', on_delete=models.PROTECT)
    client = models.ForeignKey(Clients, verbose_name='Client', on_delete=models.PROTECT)
    text = models.TextField(verbose_name='Text')
    rating = models.PositiveIntegerField(verbose_name='Rating', validators=[
                MaxValueValidator(5),
                MinValueValidator(0)
            ])

    def __str__(self):
        return f'{self.client} | {self.product}'

    class Meta:
        verbose_name = 'Products review'
        verbose_name_plural = 'Products reviews'





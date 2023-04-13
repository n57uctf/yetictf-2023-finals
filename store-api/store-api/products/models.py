from django.db import models
from clients.models import Clients
from django.core.validators import MaxValueValidator, MinValueValidator


class Products(models.Model):
    """
    This models contains records of products
    """
    name = models.CharField(verbose_name='Name', max_length=255)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='Price', default=3000, validators=[
                MaxValueValidator(1_000_000),
                MinValueValidator(3000)
            ])
    is_premium = models.BooleanField(verbose_name='Is premium', default=False)
    extra_info = models.CharField(verbose_name='Extra info', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductsReviews(models.Model):
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




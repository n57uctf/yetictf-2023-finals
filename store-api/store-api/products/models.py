from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Products(models.Model):
    """
    This models contains records of products
    """
    name = models.CharField(verbose_name='Name', max_length=255)
    description = models.TextField(verbose_name='Description')
    price = models.PositiveIntegerField(verbose_name='Price', validators=[
                MaxValueValidator(1_000_000),
                MinValueValidator(3000)
            ])

    def __str__(self):
        return self.name.__str__()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

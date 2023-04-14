from django.db import models
from django.utils import timezone
from products.models import Products


class SecretKeys(models.Model):
    key = models.CharField(verbose_name='Key', max_length=1000)
    product = models.ForeignKey(Products, verbose_name='Product', on_delete=models.PROTECT, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Secret key'
        verbose_name_plural = 'Secret keys'



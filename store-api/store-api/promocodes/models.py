from django.db import models
from clients.models import Clients


class PromoCodes(models.Model):
    """
    This model contains all promocodes
    """
    code = models.CharField(verbose_name='Promocode', max_length=255)
    amount = models.PositiveIntegerField(verbose_name='Amount', default=0)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Promocode'
        verbose_name_plural = 'Promocodes'


class PromoCodesActivations(models.Model):
    """
    This module contains history of promocodes activations
    """
    client = models.ForeignKey(Clients, verbose_name='Client', on_delete=models.PROTECT)
    code = models.ForeignKey(PromoCodes, verbose_name='Promocode', on_delete=models.PROTECT)

    def __str__(self):
        return self.code.__str__()

    class Meta:
        verbose_name = 'Promocode activation'
        verbose_name_plural = 'Promocode activations'


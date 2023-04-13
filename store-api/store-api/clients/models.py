from django.db import models
from .settings import ClientsStatuses


class Clients(models.Model):
    """
    This model contains records of registered clients
    """
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    password = models.CharField(verbose_name='Password', max_length=255)
    balance = models.PositiveIntegerField(verbose_name='Balance', default=0)

    def __str__(self):
        return self.email.__str__()

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


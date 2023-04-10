from django.db import models
from clients.models import Clients


class RefreshTokens(models.Model):
    """
    This model contains refresh token for registered clients
    """
    client = models.OneToOneField(Clients, verbose_name='Client', on_delete=models.CASCADE)
    token = models.CharField(verbose_name='Token', max_length=255)

    class Meta:
        verbose_name = 'Refresh token'
        verbose_name_plural = 'Refresh tokens'

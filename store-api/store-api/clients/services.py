"""
This module contains additional functions for clients app
"""
from __future__ import annotations
from .models import Clients
from .settings import ClientsStatuses


def get_client_by_id_or_none(client_id: int) -> Clients | None:
    """Search client in `Clients` model
    and returns instance of `Clients` model if found or None instead
    :param client_id: client id in database
    :type client_id: int
    :return: instance of `Clients` model or None
    :rtype: Clients or None
    """
    return Clients.objects.filter(pk=client_id).first()


def is_client_exists(client_id: int) -> bool:
    """Check that client exists in `Clients` model
    :param client_id: client id in database
    :type client_id: int
    :return: True if exists or False instead
    :rtype: bool
    """
    return get_client_by_id_or_none(client_id) is not None


def upgrade_client_status_to_premium(client_id: int) -> Clients:
    """Upgrade client status to 'premium'
    :param client_id: client id in database
    :type client_id: int
    :raises: Clients.DoesNotExist if client does not exist
    :return: instance of `Clients` model with new status
    :rtype: Clients
    """
    client = Clients.objects.get(pk=client_id)
    client.status = ClientsStatuses.PREMIUM.value
    client.save()
    return client


def top_up_client_balance(client_id: int, amount: int) -> Clients:
    """Top up client balance
    :param client_id: client id in database
    :type client_id: int
    :param amount: top up amount
    :type amount: int
    :raises: Clients.DoesNotExist if client does not exist
    :return: instance of `Clients` model with new balance
    :rtype: Clients
    """
    client = Clients.objects.get(pk=client_id)
    client.balance += amount
    client.save()
    return client


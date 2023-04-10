"""
This module contains function to manage RefreshTokens model
"""
from __future__ import annotations
from .models import RefreshTokens


def create_refresh_token(client_id: int, token: str) -> RefreshTokens:
    """Save refresh token to database
    :param client_id: user id
    :type client_id: int
    :param token: refresh token string
    :type token: str
    :return: instance of RefreshTokens ORM object
    :rtype: RefreshTokens
    """
    return RefreshTokens.objects.create(client_id=client_id, token=token)


def update_refresh_token(client_id: int, token: str) -> RefreshTokens:
    """Update existing record in the database
    :param client_id: path to the file with questions
    :type client_id: int
    :param token: refresh token string
    :type token: str
    :raises RefreshTokens.DoesNotExists: if token does not store in the database
    :return: instance of RefreshTokens ORM object with new refresh token
    :rtype: RefreshTokens
    """
    current_token = get_refresh_token(client_id)
    current_token.token = token
    current_token.save()
    return current_token


def create_or_update_refresh_token(client_id: int, token: str) -> RefreshTokens:
    """Update existing record in the database if record exists
            otherwise create new record
    :param client_id: path to the file with questions
    :type client_id: int
    :param token: refresh token string
    :type token: str
    :raises RefreshTokens.DoesNotExists: if record does not store in the database
    :return: instance of RefreshTokens ORM object with new refresh token
    :rtype: RefreshTokens
    """
    current_token = get_refresh_token_or_none(client_id)
    if current_token is None:
        return create_refresh_token(client_id, token)
    return update_refresh_token(client_id, token)


def get_refresh_token(client_id: int) -> RefreshTokens:
    """Get record from RefreshTokens model
    :param client_id: user id
    :type client_id: int
    :raises RefreshTokens.DoesNotExists: if record does not store in the database
    :return: instance of RefreshTokens ORM object
    :rtype: RefreshTokens
    """
    return RefreshTokens.objects.get(client_id=client_id)


def get_refresh_token_or_none(client_id: int) -> RefreshTokens | None:
    """Get record from RefreshTokens model. If record does not exist returns None
    :param client_id: user id
    :type client_id: int
    :return: instance of RefreshTokens ORM object or None if record does not exist
    :rtype: RefreshTokens or None
    """
    return RefreshTokens.objects.filter(client_id=client_id).first()


def delete_refresh_token_if_exists(client_id: int) -> None:
    """Delete record of token
    :param client_id: user id
    :type client_id: int
    :return: Nothing
    :rtype: None
    """
    current_token = get_refresh_token_or_none(client_id)
    if current_token is not None:
        current_token.delete()






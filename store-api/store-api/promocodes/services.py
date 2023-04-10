"""
This module contains additional functions for promocodes app
"""
from __future__ import annotations
from typing import List
from .models import PromoCodes, PromoCodesActivations


def get_all_promo_codes() -> List[PromoCodes]:
    """Get all promocodes from `PromoCodes` model
    :return: list of promocodes
    :rtype: List[PromoCodes]
    """
    return list(PromoCodes.objects.all())


def get_promo_code_or_none(code: str) -> PromoCodes | None:
    """Search promocode in `PromoCodes` model
    and returns instance of `PromoCodes` model if found or None instead
    :param code: code string
    :type code: str
    :return: instance of `PromoCodes` model or None
    :rtype: PromoCodes or None
    """
    return PromoCodes.objects.filter(code=code).first()


def save_promo_code_activation(client_id: int, promo_code_id: int) -> PromoCodesActivations:
    """Create record in `PromoCodesActivations` model
    :param client_id: client id in database
    :type client_id: int
    :param promo_code_id: promocode id in database
    :type promo_code_id: int
    :return: instance of `PromoCodesActivations` model
    :rtype: PromoCodesActivations
    """
    return PromoCodesActivations.objects.create(
        client_id=client_id,
        code_id=promo_code_id
    )



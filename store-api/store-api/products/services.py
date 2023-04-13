"""
This module contains additional functions for products app
"""
from __future__ import annotations
from .models import Products


def save_product(name: str, description: str, price: int) -> Products:
    """Save product to `Products` model
    :param name: product name
    :type name: str
    :param description: product description
    :type description: str
    :param price: product price (in range from 3000 to 1_000_000)
    :type price: int
    :raises ValidationError: if price not in [3000, 1_000_000] range
    :return: instance of `Products` model
    :rtype: Products
    """
    return Products.objects.create(
        name=name,
        description=description,
        price=price
    )


def get_product_by_id_or_none(product_id: int) -> Products | None:
    """Search product in `Products` model
    and returns instance of `Products` model if found or None instead
    :param product_id: product id in `Products` model
    :type product_id: int
    :return: instance of `Products` model or None
    :rtype: Products or None
    """
    return Products.objects.filter(pk=product_id).first()




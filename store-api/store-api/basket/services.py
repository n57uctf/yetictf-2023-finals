"""
This module contains additional functions of basket app
"""
from typing import List
from .models import BasketProducts


def get_basket_products(client_id: int) -> List[BasketProducts]:
    """Filters basket product by client id and return list of filtered products
    :param client_id: client id in database
    :type client_id: int
    :return: list of basket products
    :rtype: List[BasketProducts]
    """
    return list(BasketProducts.objects.filter(client_id=client_id))


def save_basket_product(client_id: int, product_id: int) -> BasketProducts:
    """Save basket product into database (`BasketProducts` model)
    :param client_id: client id in database
    :type client_id: int
    :param product_id: product id in database
    :type product_id: int
    :return: instance of BasketProducts model
    :rtype: BasketProducts
    """
    return BasketProducts.objects.create(
        client_id=client_id,
        product_id=product_id,
    )


def clear_basket(client_id: int) -> None:
    """Remove all basket product of BasketProducts model
    :param client_id: client id in database
    :type client_id: int
    :return: Nothing
    :rtype: None
    """
    BasketProducts.objects.filter(client_id=client_id).delete()


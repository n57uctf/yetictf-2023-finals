"""
This module contains additional functions for products app
"""
from __future__ import annotations
from typing import List
from .models import Products, ProductsReviews


def get_product_by_id_or_none(product_id: int) -> Products | None:
    """Search product in `Products` model
    and returns instance of `Products` model if found or None instead
    :param product_id: product id in `Products` model
    :type product_id: int
    :return: instance of `Products` model or None
    :rtype: Products or None
    """
    return Products.objects.filter(pk=product_id).first()


def get_all_reviews(**filters) -> List[ProductsReviews]:
    """Filter reviews in `ProductsReviews` model and return list of found reviews
    :return:  list of found ProductsReviews
    :rtype: List[ProductsReviews]
    """
    return list(ProductsReviews.objects.filter(**filters))


def save_product_review(product_id: int, client_id: int, text: str, rating: int) -> ProductsReviews:
    """Create record in `ProductsReviews` model
    :param product_id: product id in `Products` model
    :type product_id: int
    :param client_id: client id in `Clients` model
    :type client_id: int
    :param text: text of review
    :type text: int
    :param rating: rating of review
    :type rating: int
    :return: instance of `ProductsReviews`
    :rtype: ProductsReviews
    """
    return ProductsReviews.objects.create(
        product_id=product_id,
        client_id=client_id,
        text=text,
        rating=rating
    )




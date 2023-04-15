"""
This module contains additional functions for orders app
"""
from __future__ import annotations
from typing import List
from products.models import Products
from .models import Orders, OrderProducts
from .settings import OrdersStatuses


def get_orders_by_client_id(client_id: int) -> List[Orders]:
    """Filter orders by `client_id`
    :param client_id: client id in database
    :type client_id: int
    :return: list of filtered orders
    :rtype: List[Orders]
    """
    return list(Orders.objects.filter(client_id=client_id))


def create_order(client_id: int) -> Orders:
    """Create record in `Orders` model
    :param client_id: client id in database
    :type client_id: int
    :return: instance of `Orders` model
    :rtype: Orders
    """
    return Orders.objects.create(client_id=client_id)


def save_order_products(order_id: int, order_products_id_list: List[int]) -> None:
    """Create record in `Orders` model
    :param order_id: order id in database
    :type order_id: int
    :param order_products_id_list: list ids of products
    :type order_products_id_list: List[int]
    :return: Nothing
    :rtype: None
    """
    for product_id in order_products_id_list:
        try:
            OrderProducts.objects.create(order_id=order_id, product_id=product_id)
        except:
            ...


def get_order_by_id_or_none(order_id: int) -> Orders | None:
    """Search order in `Orders` model
    and returns instance of `Orders` model if found or None instead
    :param order_id: client id in database
    :type order_id: int
    :return: instance of `Orders` model or None
    :rtype: Orders or None
    """
    return Orders.objects.filter(pk=order_id).first()


def calculate_order_amount(order_id: int) -> int:
    """Calculate order amount of `OrderProducts`
    :param order_id: client id in database
    :type order_id: int
    :return: order amount
    :rtype: int
    """
    amount = 0
    order_products = OrderProducts.objects.select_related('product').filter(
        order_id=order_id, order__status=OrdersStatuses.WAITING_FOR_PAYMENT.value)
    for order_product in order_products:
        amount += order_product.product.price
    return amount


def get_order_products(order_id: int) -> List[Products]:
    """Filter products by `order_id`
    :param order_id: order id in database
    :type order_id: int
    :return: list of filtered products
    :rtype: List[Products]
    """
    order_products = OrderProducts.objects.select_related('product').filter(order_id=order_id)
    return [order_product.product for order_product in order_products]





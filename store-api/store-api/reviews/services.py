from typing import List
from .models import Reviews


def get_all_reviews(**filters) -> List[Reviews]:
    """Filter reviews in `ProductsReviews` model and return list of found reviews
    :return:  list of found ProductsReviews
    :rtype: List[ProductsReviews]
    """
    return list(Reviews.objects.filter(**filters))


def save_review(product_id: int, client_id: int, text: str, rating: int) -> Reviews:
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
    return Reviews.objects.create(
        product_id=product_id,
        client_id=client_id,
        text=text,
        rating=rating
    )



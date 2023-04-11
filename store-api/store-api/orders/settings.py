"""
This module contains settings for orders app
"""
from enum import Enum
from typing import List, Tuple


class OrdersStatuses(Enum):
    WAITING_FOR_PAYMENT = 'waiting for payment'
    PROCESSED = 'processed'

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(choice.value, choice.name) for choice in cls]

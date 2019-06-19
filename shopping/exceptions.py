class InvalidPrice(ValueError):
    """Thrown when invalid price detected for merchandise"""


class InvalidProduct(Exception):
    """Thrown when invalid Merchandise detected"""


class InvalidCartItem(Exception):
    """Thrown when invalid shopping cart item detected"""


class InvalidCart(Exception):
    """Thrown when invalid shopping cart detected"""


class InvalidOrderString(ValueError):
    """Trown when invalid order string is detected"""

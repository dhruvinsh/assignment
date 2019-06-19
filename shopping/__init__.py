"""
This is an Shopping module, which allow to create Merchandise, add to the
cart and perform checkout which comes with detailed tax receipt

Expected input data:
    1 book at 12.49
    1 music CD at 14.99
    1 chocolate bar at 0.85
Expected categories:
    food, music, pharmacy, book
Sales Taxes Policy:
    basic sales tax: 10% but waived for book, food, pharmacy.
    import duty tax: 5% no exceptions in conjuction with basic sales tax if
                     applicable
Expected Output:
    1 book : 12.49
    1 music CD: 16.49
    1 chocolate bar: 0.85
    Sales Taxes: 1.50
    Total: 29.83


Basic interface of this package:
Merchandise:
    allow to created merchandise as an object. has attributes like name, price,
    category and imported.
CartItem:
    merchandise that added to the cart is called cart item. a data store for
    merchandise object and it keeps track of quantity, total amount(with tax)
    and tax_amount. quantities can be increased or decreased for given
    merchandise.
Cart:
    it is a collection of CartItems. allow to do checkout for given cart and
    print out expected output
"""
import logging
from logging import NullHandler

from .cart import Cart, CartItem
from .merchandise import Merchandise, categories
from .tax import SalesTaxCalculator, SalesTaxPolicy, salestax_rounding
from .tokenizer import tokenize

__version__ = 1.0
__author__ = "Dhruvin Shah"

__all__ = [
    'Cart', 'CartItem', 'Merchandise', 'categories', 'SalesTaxCalculator',
    'SalesTaxPolicy', 'salestax_rounding', 'tokenize'
]

logging.getLogger(__name__).addHandler(NullHandler())

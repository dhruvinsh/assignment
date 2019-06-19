"""
This is an Shopping module, which allow to create Merchandise, an object that
python can understand, allow to add to the cart and perform checkout on it,
which comes with detailed tax receipt.

Expected input data:
    1 book at 12.49
    1 music CD at 14.99
    1 chocolate bar at 0.85
Expected categories:
    food, music, pharmacy, book (if none of it recognize then GENERIC category
    get assigned.)
Sales Taxes Policy:
    basic sales tax: 10% but waived for book, food, pharmacy.
    import duty tax: 5% no exceptions and in conjunction with basic sales tax
                     if applicable
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

SalesTaxPolicy:
    define sales tax over merchandise based on their category

SalesTaxCalculator:
    charge sales tax based on effective applicable tax percentage.

Usage:
for example input data like, 1 music CD: 16.49, below can be done,

>>> from shopping import Merchandise
>>> music_cd = Merchandise(name='music CD', price=16.49)
>>> music_cd
Merchandise(name='music CD', price=16.49, category='music', imported=False)

>>> from shopping import Cart
>>> my_cart = Cart()
>>> my_cart.add_merchandise(music_cd)
Cart(items=[CartItem(item=Merchandise(name='music CD', price=16.49, category='music', imported=False), total=18.139999999999997, tax_amount=1.65)])
>>> my_cart.checkout()
Qty - Items                          - Amount
  1 - music CD                       - 18.14
Sales Tax            - 1.65
Total(Incl. tax)     - 18.14
>>>

Other way,
>>> from shopping import Merchandise
>>> music_cd = Merchandise(name='music CD', price=16.49)
>>> music_cd
Merchandise(name='music CD', price=16.49, category='music', imported=False)

>>> from shopping import Cart
>>> my_cart = Cart()
>>> music_cd.add_to(my_cart)
Merchandise(name='music CD', price=16.49, category='music', imported=False)
>>> my_cart.checkout()
Qty - Items                          - Amount
  1 - music CD                       - 18.14
Sales Tax            - 1.65
Total(Incl. tax)     - 18.14
>>>
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

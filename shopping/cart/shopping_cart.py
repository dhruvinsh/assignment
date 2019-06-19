import logging
from dataclasses import dataclass, field
from typing import List

from ..exceptions import InvalidCartItem, InvalidProduct
from ..merchandise import Merchandise
from ..tax import SalesTaxCalculator

logger = logging.getLogger(__name__)


@dataclass
class CartItem:
    """A cart Item is Merchandise object, with addition properties attached to it
    param: item: a merchandise
           tax_amount: automatically calculates tax amount for given item
           qty: it is possible to buy multiple quantity. provide integer value,
                default is set to one.
    """
    item: Merchandise
    total: float = None
    tax_amount: float = None
    _qty: int = field(repr=False, default=1)

    def __post_init__(self):
        if not isinstance(self.item, Merchandise):
            raise InvalidProduct('Assign proper Merchandise to item first')

        logger.debug(f"Cart item {self.item.name}: quantity - {self.qty}")
        taxation = SalesTaxCalculator(self.item)
        self.tax_amount = taxation.salestax_amount() * self.qty
        logger.debug(
            f"Cart item {self.item.name}: tax amount - {self.tax_amount}.")

        self.total = (self.item.price * self.qty) + self.tax_amount
        logger.debug(
            f"Cart item {self.item.name}: total with tax - {self.total}")

    @property
    def qty(self):
        "gets current assigned quantity"
        return self._qty

    @qty.setter
    def qty(self, number):
        "sets quantity for item"
        try:
            number = int(number)
        except ValueError:
            raise ValueError(f'Invalid Quntity found: {number}')

        if number == 1 and self.qty == 1:
            return

        logger.debug(f"Cart item {self.item.name}: quantity update - {number}")
        self._qty = number
        # perform calculation again
        self.__post_init__()


@dataclass
class Cart:
    """A data holder for multiple shopping cart items"""
    items: List[CartItem] = field(default_factory=list)

    def __post_init__(self):
        # make sure if items initialized, it has proper items
        if not isinstance(self.items, list):
            raise InvalidCartItem(
                'Invalid cart item detect, it need to be in list')

        for item in self.items:
            if not isinstance(item, CartItem):
                raise InvalidCartItem('Invalid cart item detect')

    def _validate_add_on(self, item: Merchandise):
        "allows to test add on items are proper object or not"
        if not isinstance(item, Merchandise):
            raise InvalidProduct(f'{item} is not a valid Merchandise')

    def add_merchandise(self, items: Merchandise, qty: int = 1):
        """allows to add merchandise to the cart"""
        if isinstance(items, list):
            _ = [self._validate_add_on(i) for i in items]
        else:
            self._validate_add_on(items)
            items = [items]

        for item in items:
            item = CartItem(item=item)
            item.qty = qty
            self.items.append(item)

        return self

    def cart_total(self) -> float:
        """provides a cards total, including tax"""
        total = 0.0
        for item in self.items:
            total += (item.total)
        return total

    def total_tax(self) -> float:
        """provides total tax amount occurred on carts items"""
        total = 0.0
        for item in self.items:
            total += item.tax_amount
        return total

    def checkout(self):
        """Perform checkout of the cart and provide receipt for it,
        output looks like this,
        Item: Value
        sales tax: amount round to nearest 0.05
        Total: total amount including tax
        """
        sales_tax = self.total_tax()
        total = self.cart_total()
        print(f"{'Qty':3} - {'Items':30} - Amount")
        for item in self.items:
            print(f"{item.qty:3} - {item.item.name:30} - {item.total:.2f}")
        print(f"{'Sales Tax':20} - {sales_tax:.2f}")
        print(f"{'Total(Incl. tax)':20} - {total:.2f}")

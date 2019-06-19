from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Union

from ..exceptions import InvalidCart, InvalidPrice
from .category import categories

logger = logging.getLogger(__name__)


@dataclass
class Merchandise:
    """A data holder for individual merchandise.

    merchandise can be divide in to single category, main focus category
    for us would be book, food and medical products. Which are exempted
    from sales tax. otherwise 10% sales tax get applied
    for products in any category, if it is imported it has 5% import duty.

    param: name: name of single merchandise
           price: float or string price are allowed for merchandise,
           category: merchandise can be divide in to various category
                     to determine the sales tax.
           imported: a Boolean value to show merchandise is imported or not.
                     default is False.
    """
    name: str
    price: Union[str, float]
    category: str = None
    imported: bool = False

    def __post_init__(self):
        self._validate_price()

        self.category = self._indetify_category()
        logger.debug(f"Merchandise {self.name}: category - {self.category}")

    def _validate_price(self):
        """try to validate price of assigned merchandise"""
        # lets make sure that at end of initialization we have float price
        try:
            self.price = float(self.price)
        except ValueError:
            raise InvalidPrice(f"Invalid price {self.price} for {self.name}")
        logger.debug(f"Merchandise {self.name}: price - {self.price}")

    def _indetify_category(self):
        """try to identify category of assigned merchandise"""
        # lets have a categories assign automatically
        for category, identifiers in categories.items():
            for identifier in identifiers:
                if identifier in self.name.lower():
                    return category
        logger.warning(
            f"Merchandise {self.name}, Category not define. Set to GENERIC.")
        return 'GENERIC'

    def add_to(self, cart, qty=1) -> Merchandise:
        """allows any merchandise add to shopping cart. it automatically creates
        intermediate CartItem and assign quantity to it and then
        finally add it to the cart.
        param: cart: a Cart object is required
               qty: quantity of the merchandise add to the cart"""
        from ..cart import Cart, CartItem

        if not isinstance(cart, Cart):
            raise InvalidCart("Invalid Cart detected.")

        item = CartItem(item=self)
        item.qty = qty

        cart.items.append(item)
        return self

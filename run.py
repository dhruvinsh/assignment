import logging

from dummy_orders import order_1, order_2, order_3
from shopping import Cart, Merchandise, tokenize

logging.basicConfig()

purchase_orders = [order_1, order_2, order_3]


def method_one():
    """This method uses merchandise's add_to cart method."""
    for idx, text_order in enumerate(purchase_orders, 1):
        print(f"Output {idx}:")
        order = Cart()
        for (qty, name, price, imported) in tokenize(text_order):
            merchandise = Merchandise(name=name,
                                      price=price,
                                      imported=imported)
            merchandise.add_to(order, qty)
        order.checkout()
        print('\n')


def method_two():
    """This method uses cart's add_merchandise method."""
    for idx, text_order in enumerate(purchase_orders, 1):
        print(f"Cart {idx}:")
        order = Cart()
        for (qty, name, price, imported) in tokenize(text_order):
            merchandise = Merchandise(name=name,
                                      price=price,
                                      imported=imported)
            order.add_merchandise(merchandise, qty)
        order.checkout()
        print('\n')


if __name__ == '__main__':
    method_one()

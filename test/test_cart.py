import unittest

from shopping import Cart, CartItem, Merchandise
from shopping.exceptions import InvalidCartItem, InvalidProduct


class Base(unittest.TestCase):
    def setUp(self):
        self.book = Merchandise(name='book',
                                price=1.99,
                                category='book',
                                imported=False)
        self.perfume = Merchandise(name='perfume',
                                   price='10.19',
                                   category='accessory',
                                   imported=True)
        self.music = Merchandise(name='music CD',
                                 price='5.29',
                                 category='music',
                                 imported=False)


class TestCartItem(Base):
    def test_cart_item_validity(self):
        expected = CartItem(item=Merchandise(name='book',
                                             price=1.99,
                                             category='book',
                                             imported=False),
                            total=1.99,
                            tax_amount=0.0,
                            _qty=1)
        cart_item = CartItem(self.book)
        self.assertEqual(cart_item, expected)

    def test_cart_item_failure(self):
        with self.assertRaises(InvalidProduct):
            CartItem('Product')

    def test_cart_item_price_with_tax(self):
        cart_item = CartItem(self.perfume)
        self.assertEqual(cart_item.total, 11.74)
        self.assertEqual(cart_item.tax_amount, 1.55)

    def test_cart_item_quantity(self):
        cart_item = CartItem(self.music)
        self.assertEqual(cart_item.qty, 1)
        self.assertEqual(cart_item.total, 5.84)
        self.assertEqual(cart_item.tax_amount, 0.55)
        cart_item.qty = 10
        self.assertEqual(cart_item.qty, 10)
        self.assertEqual(cart_item.total, 58.4)
        self.assertEqual(cart_item.tax_amount, 5.5)

    def test_cart_item_quantity_failure(self):
        cart_item = CartItem(self.music)
        with self.assertRaises(ValueError):
            cart_item.qty = 'ten'


class TestCart(Base):
    def setUp(self):
        super().setUp()
        self.cart_item_book = CartItem(self.book)
        self.cart_item_perfume = CartItem(self.perfume)
        self.cart_item_music = CartItem(self.music)

    def test_cart_validity(self):
        expected = [
            CartItem(item=Merchandise(name='book',
                                      price=1.99,
                                      category='book',
                                      imported=False),
                     total=1.99,
                     tax_amount=0.0),
            CartItem(item=Merchandise(name='perfume',
                                      price=10.19,
                                      category='accessory',
                                      imported=True),
                     total=11.74,
                     tax_amount=1.55)
        ]
        items = [self.cart_item_book, self.cart_item_perfume]
        cart = Cart(items)
        self.assertEqual(cart.items, expected)

    def test_cart_failure(self):
        with self.assertRaises(InvalidCartItem):
            Cart(self.book)

        with self.assertRaises(InvalidCartItem):
            Cart([self.book, self.music])

    def test_cart_add_merchandise(self):
        expected_1 = self.cart_item_book
        expected_1.qty = 10
        cart = Cart()
        cart.add_merchandise(self.book, qty=10)
        self.assertEqual(cart.items, [expected_1])

        cart = Cart()
        cart.add_merchandise([self.book, self.perfume])
        expected_2 = self.cart_item_perfume
        expected_1 = self.cart_item_book
        expected_1.qty = 1
        self.assertEqual(cart.items, [expected_1, expected_2])

    def test_cart_add_merchandise_failure(self):
        cart = Cart()
        with self.assertRaises(InvalidProduct):
            cart.add_merchandise('Product')

    def test_cart_total(self):
        cart = Cart()
        cart.add_merchandise([self.book, self.perfume])
        self.assertEqual(cart.cart_total(), 13.73)

    def test_cart_total_tax(self):
        cart = Cart([self.cart_item_book, self.cart_item_perfume])
        self.assertEqual(cart.total_tax(), 1.55)

    def test_checkout(self):
        import sys
        from io import StringIO

        expected = [
            'Qty - Items                          - Amount',
            '  1 - book                           - 1.99',
            '  1 - perfume                        - 11.74',
            'Sales Tax            - 1.55', 'Total(Incl. tax)     - 13.73', ''
        ]

        original_stdout = sys.stdout
        sys.stdout = StringIO()
        cart = Cart([self.cart_item_book, self.cart_item_perfume])
        cart.checkout()
        result = sys.stdout.getvalue()
        sys.stdout = original_stdout
        result = result.split('\n')

        self.assertEqual(result, expected)

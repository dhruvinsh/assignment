import unittest

from shopping import Cart, CartItem, Merchandise
from shopping.exceptions import InvalidCart, InvalidPrice


class TestMerchandise(unittest.TestCase):
    def setUp(self):
        self.book = Merchandise(name='book',
                                price=1.99,
                                category='book',
                                imported=False)

    def test_valid_merchandise(self):
        self.assertEqual(self.book.name, 'book')
        self.assertEqual(self.book.price, 1.99)
        self.assertEqual(self.book.category, 'book')
        self.assertEqual(self.book.imported, False)

    def test_valid_automatic_category(self):
        book = Merchandise(name='book', price=1.99)
        self.assertEqual(book.category, 'book')

    def test_generic_category(self):
        random = Merchandise(name='Random', price=1.99)
        self.assertEqual(random.category, 'GENERIC')

    def test_merchandise_invalid_price(self):
        with self.assertRaises(InvalidPrice):
            Merchandise(name='perfume', price="ten dollar")

    def test_merchandise_add_to_cart(self):
        expected = [
            CartItem(item=Merchandise(name='book',
                                      price=1.99,
                                      category='book',
                                      imported=False),
                     total=3.98,
                     tax_amount=0.0,
                     _qty=2)
        ]
        cart = Cart()
        self.book.add_to(cart, 2)
        self.assertEqual(cart.items, expected)

    def test_merchandise_add_to_failure(self):
        cart = CartItem(self.book)
        with self.assertRaises(InvalidCart):
            self.book.add_to(cart)

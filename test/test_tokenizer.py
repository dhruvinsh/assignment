import unittest

from shopping import tokenize
from shopping.exceptions import InvalidOrderString

text_order_1 = """3 books at 2.99
                  2 music CD (imported) at 6.29"""
text_order_2 = """1 imported perfume at 7.99"""
invalid_text_order = """1 perfume 3.99"""


class TestTokenize(unittest.TestCase):
    def test_tokenize_1_validation(self):
        expected = [(3, 'books', 2.99, False),
                    (2, 'music CD (imported)', 6.29, True)]
        result = []
        for qty, name, price, imported in tokenize(text_order_1):
            result.append((qty, name, price, imported))
        self.assertEqual(result, expected)

    def test_tokenize_2_validation(self):
        for qty, name, price, imported in tokenize(text_order_2):
            pass
        self.assertEqual(qty, 1)
        self.assertEqual(name, 'imported perfume')
        self.assertEqual(price, 7.99)
        self.assertEqual(imported, 1)

    def test_tokenize_failure(self):
        generator = tokenize(invalid_text_order)
        with self.assertRaises(InvalidOrderString):
            next(generator)

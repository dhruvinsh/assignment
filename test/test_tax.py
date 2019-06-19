import unittest

from shopping import (Merchandise, SalesTaxCalculator, SalesTaxPolicy,
                      salestax_rounding)
from shopping.exceptions import InvalidProduct


class TestTaxRounding(unittest.TestCase):
    def test_amount_2_11(self):
        self.assertEqual(salestax_rounding(2.11), 2.1)

    def test_amount_2_125(self):
        self.assertEqual(salestax_rounding(2.125), 2.15)

    def test_amount_2_10(self):
        self.assertEqual(salestax_rounding(2.10), 2.1)

    def test_amount_2_13(self):
        self.assertEqual(salestax_rounding(2.13), 2.15)

    def test_amount_0_5625(self):
        self.assertEqual(salestax_rounding(0.5625), 0.55)

    def test_amount_string_2_18(self):
        self.assertEqual(salestax_rounding(2.18, string=True), '2.20')


class TestSalesTax(unittest.TestCase):
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

    def test_sales_tax_book(self):
        policy = SalesTaxPolicy(self.book)
        self.assertEqual(policy.effective_tax, 0.0)

    def test_sales_tax_perfume(self):
        policy = SalesTaxPolicy(self.perfume)
        self.assertEqual(policy.effective_tax, 15.0)

    def test_sales_tax_music(self):
        policy = SalesTaxPolicy(self.music)
        self.assertEqual(policy.effective_tax, 10.0)

    def test_sales_tax_failure(self):
        policy = SalesTaxPolicy("perfume")
        with self.assertRaises(InvalidProduct):
            policy.effective_tax

    def test_sales_tax_amount_book(self):
        tax_calculator = SalesTaxCalculator(self.book)
        self.assertEqual(tax_calculator.salestax_amount(), 0.0)

    def test_sales_tax_amount_perfume(self):
        tax_calculator = SalesTaxCalculator(self.perfume)
        self.assertEqual(tax_calculator.salestax_amount(), 1.55)

    def test_sales_tax_amount_failure(self):
        tax_calculator = SalesTaxCalculator("perfume")
        self.assertRaises(AttributeError, tax_calculator.salestax_amount)

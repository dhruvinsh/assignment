from dataclasses import dataclass

from ..exceptions import InvalidProduct
from ..merchandise import Merchandise

# for goods there is 10% basic sales tax except books, food and medical
# products. but all imported goods has 5% of duty, with no exception.
BASIC_SALES_TAX = 10.0
IMPORT_DUTY_TAX = 5.0

# categories that are exempted from sales tax
TAX_EXEMPTION_CATEGORY = ['book', 'food', 'pharmacy']


@dataclass
class SalesTaxPolicy:
    "This class forms a sales tax policy for given merchandise"
    merchandise: Merchandise

    @property
    def effective_tax(self):
        """gets effective tax percentage for given merchandise.

        Based on merchandise category sales tax policy get applied.
        Categories like book, food and medical products are exempted from
        sales tax. otherwise 10% sales tax get applied

        for products in any category, if it is imported it has 5% import duty.
        param: merchandise: takes product object for product evaluate.
        """
        if not isinstance(self.merchandise, Merchandise):
            raise InvalidProduct('Invalid Product detected')

        applicable_tax = 0.0
        if self.merchandise.imported:
            applicable_tax += IMPORT_DUTY_TAX
        if self.merchandise.category not in TAX_EXEMPTION_CATEGORY:
            applicable_tax += BASIC_SALES_TAX
        return applicable_tax

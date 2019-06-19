from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from .policy import SalesTaxPolicy


def salestax_rounding(value, string=False, nearest=0.05):
    """It allows to convert sales tax value to nearest decimal value.
    param: value: float value
           string: result in string or float. default it is set to float.
           nearest: closest value to round to.
    return: float or string with value adjusted to nearest value

    >>> salestax_rounding(2.11)
    2.1
    >>> salestax_rounding(2.125)
    2.15
    >>> salestax_rounding(2.10)
    2.1
    >>> salestax_rounding(2.13)
    2.15
    >>> salestax_rounding(0.5625)
    0.55
    """
    # we need precision up to 2 decimal points
    precision = Decimal("1.00")

    val = float(
        Decimal(f'{value}').quantize(precision, rounding=ROUND_HALF_UP))
    val = round(val / nearest) * nearest
    val = f'{val:.2f}'

    if string:
        return val
    return float(val)


@dataclass
class SalesTaxCalculator(SalesTaxPolicy):
    "Allows to calculate sales tax for merchandise."

    def salestax_amount(self) -> float:
        """allows to calculate sales tax on merchandise price.
        param: price: cost of merchandise
               applicable_tax: based on tax policy tax on product"""
        tax_amt = (self.merchandise.price * self.effective_tax) / 100
        return salestax_rounding(tax_amt)

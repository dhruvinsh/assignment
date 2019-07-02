[![Build Status](https://travis-ci.org/dhruvinsh/sales_tax.svg?branch=master)](https://travis-ci.org/dhruvinsh/sales_tax)
[![codecov](https://codecov.io/gh/dhruvinsh/sales_tax/branch/master/graph/badge.svg)](https://codecov.io/gh/dhruvinsh/sales_tax)


Note: Tested with python 3.7.3 only.


# About
Above package is to try to solve below task, and shows thought process to tackle it.  

# Task
Basic sales tax is applicable at a rate of 10% on all goods, except books, food, and medical products, which are exempt (think about how you would categorize products in this way). Import duty is an additional sales tax applicable on all imported goods at a rate of 5%, with no exemptions.

When I purchase items I receive a receipt which lists the name of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid. The rounding rules for sales tax are that for a tax rate of n%, a shelf price of p contains (np/100 rounded up to the nearest 0.05) amount of sales tax.

Write an application that prints out the receipt details for these shopping baskets.

INPUT:

``` text
Input 1:
1 book at 12.49
1 music CD at 14.99
1 chocolate bar at 0.85

Input 2:
1 imported box of chocolates at 10.00
1 imported bottle of perfume at 47.50

Input 3:
1 imported bottle of perfume at 27.99
1 bottle of perfume at 18.99
1 packet of headache pills at 9.75
1 box of imported chocolates at 11.25
```

OUTPUT:

``` text
Output 1:
1 book : 12.49
1 music CD: 16.49
1 chocolate bar: 0.85
Sales Taxes: 1.50
Total: 29.83

Output 2:
1 imported box of chocolates: 10.50
1 imported bottle of perfume: 54.65
Sales Taxes: 7.65
Total: 65.15

Output 3:
1 imported bottle of perfume: 32.19
1 bottle of perfume: 20.89
1 packet of headache pills: 9.75
1 imported box of chocolates: 11.85
Sales Taxes: 6.70
Total: 74.68
```

# Brainstorming
From above task, we can say that there is certain **tax policy**. There are two type of tax, **basic sales tax** and **import duty tax** and it is applicable based on merchandise category. Categories like book, food and medical products are exempted from sales tax. otherwise 10% sales tax get applied for products in any category. If any merchandise is imported it has 5% import duty disregarding its category. At the end, applicable tax on the merchandise get rounded to nearest **0.05** and get added to Merchandise price.


Then there are different kinds of **Merchandise**, we can see that from input data. One of the line is `1 imported bottle of perfume at 47.50`. observing this line, it is obvious that, first part is integer which represents quantity, then one or more string separated by space till "at" word appears, that's a product name. and after "at" there is float value which represents price. In a product name you can find "imported" word, which gives idea about if merchandise is imported or not.


On purchase of collection of merchandise, receipt get generated, where item price includes tax amount. Above mentioned line come up in receipt as `1 imported bottle of perfume: 54.65`. At the end it shows total sales tax (basic sales tax and import duty tax together) paid for given collection of items. And Grand total as well. 

### Design

So to cover all, in `shopping` package there are 3 components, Tax Policy, Merchandise and Shopping Cart.

Based on Input data, we can parse needed data and generate merchandise objects. tokenizer is there to parse the string order and help us to generate merchandise objects.

Merchandise has name, price, category and imported status. Based on observed input data we have some predefined merchandise category as well. Category get assigned automatically from statically defined categories, if it not found then GENERIC category get assigned.

Merchandise added to Cart, it called CartItem. CartItem provides data holder for merchandise itself and it's total amount with tax, tax amount and quantity. all these calculation done automatically since we have needed information assigned in Merchandise object, and predefined tax policy.

Collection of the CartItem get stored in Cart, from there checkout can be performed and print above output.


### Manual Calculation

Since there is low number of input data lets do calculation manually.

Items: things that are bought  
Net Price: shelf price of the items  
Sales Tax: in percentage, based on Product category.  
Import Duty: in percentage  
Effective Tax: Addition of Sales Tax and Import Duty.  
Tax Amt: based on effective tax percentage, tax amount need to pay over price  
Gross Price: Net Price + Tax Amt  
Corrected Tax Amt: rounding tax amount to nearest 0.05(according to task)  
Corrected Gross Price: Net Price + Corrected Tax Amt  


| Items               | Net price | Sales Tax | Import Duty | Effective Tax | Tax Amt | Gross Price | Corrected Tax Amt | Corrected Gross Price | 
|---------------------|-----------|-----------|-------------|---------------|---------|-------------|-------------------|-----------------------| 
| Input 1:            |           |           |             |               |         |             |                   |                       | 
| book                | 12.49     | 0         | 0           | 0             | 0       | 12.49       | 0                 | 12.49                 | 
| music               | 14.99     | 10        | 0           | 10            | 1.499   | 16.489      | 1.5               | 16.49                 | 
| chocolate bar       | 0.85      | 0         | 0           | 0             | 0       | 0.85        | 0                 | 0.85                  | 
| Total               |           |           |             |               | 1.499   | 29.829      | 1.5               | 29.83                 | 
|                     |           |           |             |               |         |             |                   |                       | 
| Input 2:            |           |           |             |               |         |             |                   |                       | 
| imported chocolates | 10        | 0         | 5           | 5             | 0.5     | 10.5        | 0.5               | 10.5                  | 
| imported perfume    | 47.5      | 10        | 5           | 15            | 7.125   | 54.625      | 7.15              | 54.65                 | 
| Total               |           |           |             |               | 7.625   | 65.125      | 7.65              | 65.15                 | 
|                     |           |           |             |               |         |             |                   |                       | 
| Input 3:            |           |           |             |               |         |             |                   |                       | 
| imported perfume    | 27.99     | 10        | 5           | 15            | 4.1985  | 32.1885     | 4.2               | 32.19                 | 
| perfume             | 18.99     | 10        | 0           | 10            | 1.899   | 20.889      | 1.9               | 20.89                 | 
| headache pills      | 9.75      | 0         | 0           | 0             | 0       | 9.75        | 0                 | 9.75                  | 
| imported chocolates | 11.25     | 0         | 5           | 5             | 0.5625  | 11.8125     | 0.55              | 11.8                  | 
| Total               |           |           |             |               | 6.66    | 74.64       | 6.65              | 74.63                 | 


### Issue
There is one issue found, `1 imported chocolates at 11.25` is belongs to food category and is imported, so effective tax would be 5% and tax amount would be 0.5625. And nearest round amount would be 0.55, not 0.60 as it shows in output 3: `1 imported box of chocolates: 11.85`.

Rounding Method 1: (incorrect)
``` python
>>> import math
>>> 11.25 * 0.05
0.5625
>>> math.ceil(0.5625 / 0.05) * 0.05
0.6000000000000001
```


Rounding Method 2: (correct)

``` python
>>> from decimal import ROUND_HALF_UP, Decimal
>>> precision = Decimal("1.00")
>>> val = float(Decimal('0.5625').quantize(precision, rounding=ROUND_HALF_UP))
>>> val = round(val / 0.05) * 0.05
>>> val
0.55
```

# Running Application
Get a copy of the project, make sure you have git installed and it is in path, run below command,

``` text
git clone https://github.com/dhruvinsh/sales_tax.git
```


I am using **pipenv** environment manager. Below command install needed dependency automatically.
### Dependency
Run below command from command line from the project directory.

``` text
pip install pipenv
```

``` text
pipenv install
```
### Running
Make sure you have pipenv in path and cmd prompt in the same directory as project.

##### Unittest
``` text
pipenv run coverage run -m unittest -v
```
##### Code Coverage
``` text
pipenv run coverage report
```
##### Run Application
There are two methods to generate the output, by default it is set to run method one. change can be applied by setting method_two() in `run.py` file.
``` text
pipenv run python run.py
```

# Usage
Input data like, `1 music CD: 16.49`, below can be done,

``` python-console
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
```

Other way,

``` python-console
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
```

# Code Coverage
```text
Name                               Stmts   Miss  Cover
------------------------------------------------------
shopping\__init__.py                  10      0   100%
shopping\cart\__init__.py              2      0   100%
shopping\cart\shopping_cart.py        73      0   100%
shopping\exceptions.py                 5      0   100%
shopping\merchandise\__init__.py       3      0   100%
shopping\merchandise\category.py       1      0   100%
shopping\merchandise\products.py      37      0   100%
shopping\tax\__init__.py               3      0   100%
shopping\tax\calculation.py           16      0   100%
shopping\tax\policy.py                17      0   100%
shopping\tokenizer.py                 16      0   100%
------------------------------------------------------
TOTAL                                183      0   100%
```

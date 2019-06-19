from .exceptions import InvalidOrderString


def tokenize(order):
    """allow to break string orders to the token, made of qty, name and price.
    order text looks like as,
    1 book at 12.49
    1 music CD at 14.99
    1 chocolate bar at 0.85

    observing above data, it is obvious that, first part is integer which
    represents quantity, then one or more string separated by space till "at"
    word appears, that's a product name. and after "at" there is float value
    which represents price.

    in a product name you can find "imported" word, which gives idea about if
    merchandise is imported or not.

    this generator provide below values in sequence,
    qty: int,
    name: str,
    price: float,
    imported: bool
    """
    order = order.split('\n')
    order = [i.strip() for i in order]
    for line in order:
        try:
            imported = False
            line = line.split()
            qty = int(line[0])
            name = ' '.join(line[1:line.index('at')])
            price = float(line[-1])
            if 'imported' in name.lower():
                imported = True
            yield qty, name, price, imported
        except (IndexError, ValueError):
            raise InvalidOrderString("Invalid order string detected")

class Bed:
    _TYPE_SIZE = {"S": 0.9, "U": 1.2}

    def __init__(self, bed_type, price, description):
        self._type = bed_type
        self._price = price
        self._description = description

    @property
    def price(self):
        return self._price

    @property
    def floorArea(self):
        return self._TYPE_SIZE[self._type]

    def __str__(self):
        return f"{self._description}, ${self._price:.2f}"

from abc import ABC, abstractmethod


class Amenity(ABC):
    def __init__(self, itemCode, description, price):
        self._itemCode = itemCode
        self._description = description
        self._price = price

    @property
    def itemCode(self):
        return self._itemCode

    @property
    def price(self):
        return self._price

    @abstractmethod
    def getFloorArea(self):
        pass

    def __str__(self):
        return f"{self._itemCode}, {self._description}, ${self._price:.2f}"


class InRoomAmenity(Amenity):
    def __init__(self, itemCode, description, price, floorArea):
        super().__init__(itemCode, description, price)
        self._floorArea = floorArea

    def getFloorArea(self):
        return self._floorArea

    @property
    def floorArea(self):
        return self._floorArea


class SharedAmenity(Amenity):
    def getFloorArea(self):
        return 0


def main():
    amenities = [
        SharedAmenity("GYM-PEP", "Per entry pass to gym (Level 4-01)", 1.0),
        SharedAmenity("SPA-SOL", "30-minute spa treatment", 50.0),
        InRoomAmenity("NET-WIZ", "High-speed internet", 10.0, 0.3),
        InRoomAmenity("TV-PLS", "Pay-per-view movies", 5.0, 0.2),
    ]

    totalFloorArea = sum(a.getFloorArea() for a in amenities)
    totalPrice = sum(a.price for a in amenities)

    print(f"Total Floor Area: {totalFloorArea:.2f} m2")
    print(f"Total Price: ${totalPrice:.2f}")


if __name__ == "__main__":
    main()

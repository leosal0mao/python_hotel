from amenity import InRoomAmenity, SharedAmenity
from bed import Bed
from exception import BookingException, MinFloorAreaException


class Room:
    _MIN_EXIT_SPACE = 1.84  # in square meters
    _TYPE_SIZE = {"S": 12, "D": 16}

    def __init__(self, room_type, room_price, bed):
        self._type = room_type
        self._roomPrice = room_price
        self._bed = bed
        self._amenities = []

    @property
    def type(self):
        return self._type

    @property
    def roomPrice(self):
        return self._roomPrice

    @property
    def fullPrice(self):
        amenities_price = sum([amenity.price for amenity in self._amenities])
        return self._roomPrice + self._bed.price + amenities_price

    def addAmenity(self, newItem):
        # Check for duplicate amenity
        if newItem in self._amenities:
            raise BookingException("Duplicate amenity detected")

        # Check if minimum floor area is compromised (only for InRoomAmenity)
        if isinstance(newItem, InRoomAmenity):
            total_size = self._MIN_EXIT_SPACE + sum(
                [
                    amenity.floorArea
                    for amenity in self._amenities
                    if isinstance(amenity, InRoomAmenity)
                ]
            )
            if total_size + newItem.floorArea > self._TYPE_SIZE[self._type]:
                raise MinFloorAreaException("Minimum floor area is compromised")

        # Add the new amenity
        self._amenities.append(newItem)

    def removeAmenity(self, itemCode):
        for amenity in self._amenities:
            if amenity.itemCode == itemCode:
                self._amenities.remove(amenity)
                return
        raise BookingException("No such amenity in this room")

    def __str__(self):
        room_details = f"{self._type} room, ${self._roomPrice:.2f}\n"
        bed_details = str(self._bed)
        amenities_details = "\n".join([str(a) for a in self._amenities])
        full_price = f"\nFull Price: ${self.fullPrice:.2f}"
        return room_details + bed_details + amenities_details + full_price


def main():
    try:
        # Create Deluxe Room
        deluxe_bed = Bed("Super", 18.99, "Super single")
        standard_bed = Bed("Single", 12.99, "single")
        # Create amenities
        mini_fridge = InRoomAmenity("FRI", "Mini fridge", 10.00, 1.0)
        chair = InRoomAmenity("CHA", "Chair", 5.00, 0.5)
        writing_desk = InRoomAmenity("DSK", "Writing desk", 15.00, 2.0)
        iron_board = InRoomAmenity("IRO", "Iron and ironing Board", 12.00, 1.0)
        gym_pass = SharedAmenity("GYM", "Gym pass", 20.00)
        wifi = SharedAmenity("WIFI", "Wi-Fi", 5.00)

        # Create rooms with amenities
        deluxe_room = Room("Deluxe", 100.00, deluxe_bed)
        deluxe_room.addAmenity(mini_fridge)
        deluxe_room.addAmenity(chair)
        deluxe_room.addAmenity(writing_desk)
        deluxe_room.addAmenity(iron_board)

        standard_room = Room("Standard", 80.00, standard_bed)
        standard_room.addAmenity(gym_pass)
        standard_room.addAmenity(mini_fridge)
        standard_room.addAmenity(wifi)
        standard_room.addAmenity(gym_pass)

        # Remove Mini fridge amenity
        deluxe_room.removeAmenity("FRI")
        standard_room.removeAmenity("FRI")

        # Remove Gym pass amenity
        standard_room.removeAmenity("GYM")

        # Print room string representation
        print(deluxe_room)
        print(standard_room)

    except BookingException as e:
        print("BookingException:", e)

    except MinFloorAreaException as e:
        print("MinFloorAreaException:", e)

    except Exception as e:
        print("Exception:", e)


if __name__ == "__main__":
    main()

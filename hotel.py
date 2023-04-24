from datetime import datetime
from amenity import InRoomAmenity, SharedAmenity
from exception import BookingException
from guest import Guest


class Hotel:
    def __init__(self, name, roomFilename):
        self._name = name
        self._guests = self.setupGuests()
        self._amenities = self.setupAmenities()
        self._roomAvailability = self.setupRoomAvailability(roomFilename)
        self._bookings = {}

    def setupGuests(self):
        guests = {}
        infile = open("Guests.txt", "r")
        for line in infile:
            pp, name, country = line.split(",")
        guests[pp.strip()] = Guest(pp.strip(), name.strip(), country.strip())
        infile.close()

        infile = open("Blacklist.txt", "r")
        for line in infile:
            pp, dateReported, reason = line.split(",")
        g = guests.get(pp.strip())
        if g is not None:
            g.blacklist(
                datetime.strptime(dateReported.strip(), "%d-%b-%Y").date(),
                reason.strip(),
            )

        infile.close()
        return guests

    def setupAmenities(self):
        amenities = []
        infile = open("SharedAmenity.txt", "r")
        for line in infile:
            itemCode, desc, price = line.split(",")
        amenities.append(SharedAmenity(itemCode, desc, float(price)))
        infile.close()

        infile = open("InRoomAmenity.txt", "r")
        for line in infile:
            itemCode, desc, price, floorArea = line.split(",")
        amenities.append(InRoomAmenity(itemCode, desc, float(price), float(floorArea)))
        infile.close()
        return amenities

    def setupRoomAvailability(self, filename):
        roomAvailability = {}
        infile = open(filename, "r")
        for line in infile:
            dateString, standardCount, deluxeCount = line.split(",")
            thisDate = datetime.strptime(dateString, "%d-%b-%Y").date()
            roomAvailability[thisDate] = [int(standardCount), int(deluxeCount)]
        infile.close()
        return roomAvailability

    def saveRoomAvailability(self, filename):
        outfile = open(filename, "w")
        for k, v in self._roomAvailability.items():
            print("{},{},{}".format(k.strftime("%d-%b-%Y"), v[0], v[1]), file=outfile)
        outfile.close()

    def searchGuest(self, passport):
        for guest in self._guests.values():
            if guest.passport == passport:
                return guest
        return None

    def checkRoomAvailability(self, start, end, roomType):
        if (
            start > end
            or start not in self._roomAvailability
            or end not in self._roomAvailability
        ):
            return False
        roomCount = self._roomAvailability[start][
            roomType
        ]  # roomType can be either 0 or 1 for standard and deluxe
        for date in range(start, end):
            if (
                date not in self._roomAvailability
                or self._roomAvailability[date][roomType] < roomCount
            ):
                return False
        return True

    def listAmenity(self):
        return "\n".join([str(amenity) for amenity in self._amenities])

    def getAmenity(self, itemCode):
        for amenity in self._amenities:
            if amenity.itemCode == itemCode:
                return amenity
        return None

    def searchBooking(self, bookingID):
        if bookingID in self._bookings:
            return self._bookings[bookingID]
        else:
            return None

    def searchBookingByPassport(self, passport):
        bookings = []
        for booking in self._bookings.values():
            if booking.guest.passport == passport:
                bookings.append(booking)
        return bookings

    def submitBooking(self, newBooking):
        if newBooking.status != "Pending":
            raise BookingException("Booking status must be Pending.")
        if not self.checkRoomAvailability(
            newBooking.checkInDate, newBooking.checkOutDate, newBooking.room.type
        ):
            raise BookingException(
                "Room is not available for the given dates and room type."
            )
        roomType = newBooking.room.type
        for date in range(newBooking.checkInDate, newBooking.checkOutDate):
            self._roomAvailability[date][roomType] -= 1
        newBooking.status = "Confirmed"
        self._bookings[newBooking.bookingID] = newBooking

    def cancelBooking(self, bookingID):
        if bookingID not in self._bookings:
            raise BookingException("No booking found with the given ID.")
        booking = self._bookings[bookingID]
        if booking.status != "Confirmed":
            raise BookingException("Booking is not confirmed and cannot be cancelled.")
        roomType = booking.room.type
        for date in range(booking.checkInDate, booking.checkOutDate):
            self._roomAvailability[date][roomType] += 1
        booking.status = "Cancelled"

    def checkIn(self, bookingID, allocatedRoomNo):
        booking = self._bookings[bookingID]
        if not booking:
            raise BookingException("No booking found with the given ID.")
        booking.checkIn(self, allocatedRoomNo)

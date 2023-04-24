from datetime import date
from exception import BookingException
from room import Room
from guest import Guest


class Booking:
    _NEXT_ID = 1

    def __init__(self, guest, room, check_in_date, check_out_date):
        if guest.is_blacklisted():
            raise BookingException("Guest is blacklisted")

        if check_out_date <= check_in_date:
            raise BookingException("Check-out date must be after check-in date")

        self._bookingID = str(Booking._NEXT_ID)
        Booking._NEXT_ID += 1
        self._guest = guest
        self._room = room
        self._checkInDate = check_in_date
        self._checkOutDate = check_out_date
        self._allocatedRoomNo = None
        self._status = "Pending"

    @property
    def bookingID(self):
        return self._bookingID

    @property
    def checkInDate(self):
        return self._checkInDate

    @property
    def checkOutDate(self):
        return self._checkOutDate

    @property
    def status(self):
        return self._status

    @property
    def passport(self):
        return self._guest.passport

    @property
    def roomType(self):
        return self._room.roomType

    @property
    def totalPrice(self):
        num_nights = (self._checkOutDate - self._checkInDate).days
        return self._room.fullPrice * num_nights

    @status.setter
    def status(self, value):
        self._status = value

    def checkIn(self, allocated_room_no):
        if self._status != "Confirmed":
            raise BookingException("Booking is not confirmed")

        if date.today() != self._checkInDate:
            raise BookingException("Check-in can only be done on the check-in date")

        if self._guest.is_blacklisted():
            raise BookingException("Guest is blacklisted")

        self._status = "Checked-In"
        self._allocatedRoomNo = allocated_room_no

    def __str__(self):
        room_str = str(self._room)
        return (
            f"Booking ID: {self._bookingID}\n"
            f"Passport Number: {self._guest.passport}\n"
            f"Name: {self._guest.name}\n"
            f"Check-In/Out dates: {self._checkInDate.strftime('%d-%b-%Y')} / "
            f"{self._checkOutDate.strftime('%d-%b-%Y')}\n"
            f"Booking Status: {self._status}\n"
            f"{room_str}\n"
            f"Total Price: {self.totalPrice:.2f} x "
            f"{(self._checkOutDate - self._checkInDate).days} nights = "
            f"{self.totalPrice * (self._checkOutDate - self._checkInDate).days:.2f}"
        )

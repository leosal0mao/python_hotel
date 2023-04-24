import atexit
from bed import Bed
from hotel import Hotel
from room import Room
from booking import Booking


class SAMIhotel:
    def __init__(self):
        # Prompt user to enter filename containing room availability information.
        filename = input("Enter filename containing room availability information: ")

        # Create the Hotel object for SAMI
        self.hotel = Hotel("SAMI", filename)

        # Invoke the appropriate Hotel method to perform the room availability setup.
        self.hotel.setupRoomAvailability(filename)

        # The same filename will be used to save the latest room availability information before the application exits.
        atexit.register(self.hotel.saveRoomAvailability, filename)

    def main(self):
        print("========== SAMI Hotel ==========")

        while True:
            print("1. Submit Booking")
            print("2. Cancel Booking")
            print("3. Search Booking(s)")
            print("4. Check-In")
            print("0. Exit")
            option = input("Enter option: ")

            if option == "1":
                self.submit_booking()
            elif option == "2":
                self.cancel_booking()
            elif option == "3":
                self.search_booking()
            elif option == "4":
                self.check_in()
            elif option == "0":
                print("Exiting program...")
                break
            else:
                print("Invalid option. Please try again.")

    ################## STEP 1 - BOOKING
    def submit_booking(self):
        # Prompt for guest passport to locate the Guest object
        passport = input("Enter passport number to start: ")
        guest = self.hotel.searchGuest(passport)

        # If guest is not found, display appropriate message and return to menu
        if guest is None:
            print("Guest not found. Please register guest first.")
            return

        # Print guest details for verification
        print("Guest located, please verify:")
        print(guest)

        # Prompt user to enter room and bed type
        room_type = input("Select preferred room type (S)tandard or (D)eluxe): ")
        bed_type = input("Select preferred bed type (S)ingle or s(U)per: ")

        # Create Room object with selected Bed object
        room = Room(room_type, Bed(bed_type))

        # List hotel's amenities for guest to include in the booking
        print("Please select amenities to include in the booking:")
        for code, amenity in self.hotel.amenities.items():
            print(f"{code}. {amenity.name} (${amenity.price:.2f})")

        # Prompt guest for item code to add to room
        while True:
            code = input("Enter item code to add or <enter> to stop: ")
            if code == "":
                break

            # If the item code is valid, add the Amenity object to the room
            if code in self.hotel.amenities:
                room.addAmenity(self.hotel.amenities[code])
            else:
                print("Invalid amenity code.")

        # Ask for Check-In and Check-Out date
        check_in = input("Enter Check-In date in DD-MON-YYYY: ")
        check_out = input("Enter Check-Out date in DD-MON-YYYY: ")

        # Create Booking object using data/objects collected above
        booking = Booking(guest, room, check_in, check_out)

        # Display booking details for verification and prompt user for confirmation
        print("Booking details:")
        print(booking)
        confirm = input("Proceed to submit booking? (Y/N): ")

        # If yes, proceed to submit this new booking
        if confirm.lower() == "y":
            self.hotel.submitBooking(booking)
            print("Booking submitted successfully.")
        # If no, display message that this booking is aborted
        else:
            print(f"There is no Deluxe room available from {check_in} to {check_out}")

    ################## STEP 2 - CANCEL BOOKING
    def cancel_booking(self):
        booking_id = input("Enter booking ID number: ")
        booking = self.hotel.searchBooking(booking_id)
        if booking:
            print("Booking Details:")
            print(booking)
            confirmation = input("Confirm cancellation? (y/n): ")
            if confirmation.lower() == "y":
                self.hotel.cancelBooking(booking_id)
                print("Booking has been canceled.")
            else:
                print("Cancellation aborted.")
        else:
            print("Booking not found.")

    ################## STEP 3 - SEARCH BOOKING
    def search_booking(self):
        search_option = input("Search by booking ID or passport? (B/P):  ")
        if search_option == "b":
            booking_id = input("Enter booking ID: ")
            booking = self.hotel.searchBooking(booking_id)
            if booking:
                print("\nBooking details:\n")
                print(str(booking))
            else:
                print("Booking not found.")
        elif search_option == "p":
            passport = input("Enter guest passport: ")
            bookings = self.hotel.searchBookingByPassport(passport)
            if bookings:
                print("\nBooking details:\n")
                for booking in bookings:
                    print(str(booking))
            else:
                print("No bookings found for this guest.")
        else:
            print("Invalid option.")

    ################## STEP 4 - CHECKIN
    def check_in(self):
        booking_id = input("Enter booking ID to start checkin: ")

        # Locate booking object
        booking = self.hotel.searchBooking(booking_id)
        if not booking:
            print("Booking not found.")
            return

        # Display booking details
        print("\nBooking Details:")
        print(booking)

        # Prompt for room number
        room_number = input(
            "Enter allocated room number or press <enter> to cancel Check-In:"
        )
        if not room_number:
            print("Check-In cancelled.")
            return

        # Perform check-in
        success = self.hotel.submitBooking(booking_id, room_number)
        if success:
            print("Checked-In. Enjoy your stay in SAMI")
        else:
            print("Cannot check-in today!!")


if __name__ == "__main__":
    hotel = SAMIhotel()
    hotel.main()

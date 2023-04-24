from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext

from guest import Guest


class BlacklistGUI:
    def __init__(self, master):
        self.current_passport = None
        self.master = master
        master.title("SAMI Blacklist GUI - done by")

        # Load guests and blacklists from files
        self.guests = {}
        with open("Guests.txt") as f:
            for line in f:
                passport, name, country = line.strip().split(",")
                self.guests[passport] = {
                    "name": name,
                    "country": country,
                }
        self.blacklists = {}
        with open("Blacklist.txt") as f:
            for line in f:
                passport, date, reasons = line.strip().split(",", 2)
                self.blacklists[passport] = {"date": date, "reasons": reasons}

        # Passport label and entry
        self.passport_label = tk.Label(master, text="Passport:")
        self.passport_label.grid(row=0, column=0)
        self.passport_entry = tk.Entry(master)
        self.passport_entry.grid(row=0, column=1)

        # Date Reported label and entry
        self.date_label = tk.Label(master, text="Date Reported: (dd-mon-yyyy)")
        self.date_label.grid(row=1, column=0)
        self.date_entry = tk.Entry(master)
        self.date_entry.grid(row=1, column=1)

        # Reason label and entry
        self.reason_label = tk.Label(master, text="Reason(s):")
        self.reason_label.grid(row=2, column=0)
        self.reason_entry = tk.Entry(master)
        self.reason_entry.grid(row=2, column=1)

        # Search button
        self.search_button = tk.Button(master, text="Search", command=self.search_guest)
        self.search_button.grid(row=3, column=0)

        # Blacklist button
        self.blacklist_button = tk.Button(
            master, text="Blacklist", command=self.blacklist_guest, state="disabled"
        )
        self.blacklist_button.grid(row=3, column=1)

        # Reset button
        self.reset_button = tk.Button(
            master, text="Reset", command=self.reset_fields, state="disabled"
        )
        self.reset_button.grid(row=3, column=2)

        # Scrolled text
        self.scrolled_text = tk.scrolledtext.ScrolledText(
            master, height=10, state="disabled"
        )
        self.scrolled_text.grid(row=4, columnspan=3)

    def search_guest(self):
        passport = self.passport_entry.get()
        if passport in self.guests:
            # Display guest information
            guest_info = f"Name: {self.guests[passport]['name']}\n"
            guest_info += f"Country: {self.guests[passport]['country']}\n\n"
            self.scrolled_text.config(state="normal")
            self.scrolled_text.delete("1.0", tk.END)
            self.scrolled_text.insert(tk.END, guest_info)
            self.scrolled_text.config(state="disabled")

            # Enable text entries for date and reason
            self.date_entry.config(state="normal")
            self.reason_entry.config(state="normal")

            # Disable passport entry and search button
            self.passport_entry.config(state="disabled")
            self.search_button.config(state="disabled")

            # Enable reset button
            self.reset_button.config(state="normal")

            # Enable blacklist button
            self.blacklist_button.config(state="normal")
            self.current_passport = passport

        else:
            # Display error message
            error_message = "Guest not found!"
            self.scrolled_text.config(state="normal")
            self.scrolled_text.delete("1.0", tk.END)
            self.scrolled_text.insert(tk.END, error_message)
            self.scrolled_text.config(state="disabled")

            # Disable text entries for date and reason
            self.date_entry.config(state="disabled")
            self.reason_entry.config(state="disabled")

            # Enable passport entry and search button
            self.passport_entry.config(state="normal")
            self.search_button.config(state="normal")

            # Disable reset and blacklist buttons
            self.reset_button.config(state="disabled")
            self.blacklist_button.config(state="disabled")

    def blacklist_guest(self):
        passport = self.passport_entry.get()
        date = self.date_entry.get()
        reasons = self.reason_entry.get()

        if not all([self.date_entry.get(), self.reason_entry.get()]):
            # Display error message if any field is empty
            error_message = "Please fill in all fields!"
            self.scrolled_text.config(state="normal")
            self.scrolled_text.delete("1.0", tk.END)
            self.scrolled_text.insert(tk.END, error_message)
            self.scrolled_text.config(state="disabled")
            return

        if passport in self.blacklists:
            # Update existing blacklist entry
            date = datetime.strptime(date, "%d-%b-%Y").strftime("%d-%b-%Y")
            self.blacklists[passport]["date"] = date
            self.blacklists[passport]["reasons"] = reasons
        else:
            # Create new blacklist entry
            self.blacklists[passport] = {"date": date, "reasons": reasons}

        # Update guest's blacklisted attribute
        guest = Guest(
            passport, self.guests[passport]["name"], self.guests[passport]["country"]
        )
        guest.blacklist(date, reasons)

        # Display updated guest information
        guest_info = f"Name: {guest.name}\n"
        guest_info += f"Country: {guest.country}\n"
        guest_info += f"Blacklisted: {''.join(map(str, guest._blacklistedReason))}\n\n"
        self.scrolled_text.config(state="normal")
        self.scrolled_text.delete("1.0", tk.END)
        self.scrolled_text.insert(tk.END, guest_info)
        self.scrolled_text.config(state="disabled")

        # Save guest's information to file
        with open("Guests.txt", "w") as f:
            for passport, guest_info in self.guests.items():
                name = guest_info["name"]
                country = guest_info["country"]
                f.write(f"{passport},{name},{country}\n")

        # Save blacklist information to file
        with open("Blacklist.txt", "w") as f:
            for passport, blacklist_info in self.blacklists.items():
                date = blacklist_info["date"]
                reasons = blacklist_info["reasons"]
                f.write(f"{passport},{date},{reasons}\n")

    def reset_fields(self):
        # Clear text entries and ScrolledText
        self.date_entry.delete(0, tk.END)
        self.reason_entry.delete(0, tk.END)
        self.scrolled_text.config(state="normal")
        self.scrolled_text.delete("1.0", tk.END)

        # Disable text entries for date and reason
        self.date_entry.config(state="disabled")
        self.reason_entry.config(state="disabled")

        # Enable passport entry and search button
        self.passport_entry.config(state="normal")
        self.search_button.config(state="normal")

        # Disable reset and blacklist buttons
        self.reset_button.config(state="disabled")
        self.blacklist_button.config(state="disabled")
        self.current_passport = None


root = tk.Tk()
blacklist_gui = BlacklistGUI(root)
root.mainloop()

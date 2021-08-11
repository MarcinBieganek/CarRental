import database as db
import dev as dev
import graphics as gp

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

class Window:
    def __init__(self, main):
        self.main = main
        self.main.show_cars()
        self.window = tk.Toplevel()
        self.window.geometry("700x500")
        self.window.title("Dodawanie klienta")
        self.window.iconbitmap(gp.ICON_PATH)
        self.window.configure(bg=gp.BG_COLOR)

        # frame for border look of the main frame
        self.border_view_frame = tk.Frame(self.window, bg=gp.BORDER_COLOR, bd=7)
        self.border_view_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        # main frame
        self.view_frame = tk.Frame(self.border_view_frame, bg=gp.BG_COLOR, bd=5)
        self.view_frame.place(relwidth=1, relheight=1)       

        # label and entry
        self.first_name_label = tk.Label(self.view_frame, text="Imie: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.first_name_label.place(relx=0.1, rely=0.15, relwidth=0.4, relheight=0.1)

        self.first_name_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.first_name_entry.place(relx=0.5, rely=0.15, relwidth=0.4, relheight=0.1)

        self.last_name_label = tk.Label(self.view_frame, text="Nazwisko: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.last_name_label.place(relx=0.1, rely=0.25, relwidth=0.4, relheight=0.1)

        self.last_name_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.last_name_entry.place(relx=0.5, rely=0.25, relwidth=0.4, relheight=0.1)

        self.city_label = tk.Label(self.view_frame, text="Miasto: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.city_label.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.1)

        self.city_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.city_entry.place(relx=0.5, rely=0.35, relwidth=0.4, relheight=0.1)

        self.email_label = tk.Label(self.view_frame, text="E-mail: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.email_label.place(relx=0.1, rely=0.45, relwidth=0.4, relheight=0.1)

        self.email_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.email_entry.place(relx=0.5, rely=0.45, relwidth=0.4, relheight=0.1)

        self.phone_number_label = tk.Label(self.view_frame, text="Nr telefonu: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.phone_number_label.place(relx=0.1, rely=0.55, relwidth=0.4, relheight=0.1)

        self.phone_number_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.phone_number_entry.place(relx=0.5, rely=0.55, relwidth=0.4, relheight=0.1)

        # buttons
        self.submit_button = tk.Button(self.view_frame, text="Dodaj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.add)
        self.submit_button.place(relx=0.2, rely=0.75, relwidth=0.3, relheight=0.1)

        self.cancel_button = tk.Button(self.view_frame, text="Anuluj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.window.destroy)
        self.cancel_button.place(relx=0.5, rely=0.75, relwidth=0.3, relheight=0.1)

    def add(self):
        error_response = ""
        first_name_regex = r"[A-Z][a-ząćęłńóśźż]{1,15}( [A-Z][a-ząćęłńóśźż]{0,15})?"
        last_name_regex = r"[A-Z][a-ząćęłńóśźż]{1,15}([ \'\-][A-Z][a-ząćęłńóśźż]{0,15})?"
        city_regex = r"[A-Z][a-ząćęłńóśźż]{1,15}([ \'\-][A-Z][a-ząćęłńóśźż]{0,15})?([ \'\-][A-Z][a-ząćęłńóśźż]{0,15})?"
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        phone_number_regex = r"\d{9}"

        r = re.match(first_name_regex, self.first_name_entry.get())
        if r == None:
            error_response = error_response + " Błąd w imieniu.\n"
        else:
            first_name = r.group(0)

        r = re.match(last_name_regex, self.last_name_entry.get())
        if r == None:
            error_response = error_response + " Błąd w nazwisku.\n"
        else:
            last_name = r.group(0)
        
        r = re.match(city_regex, self.city_entry.get())
        if r == None:
            error_response = error_response + " Błąd w mieście.\n"
        else:
            city = r.group(0)

        r = re.match(email_regex, self.email_entry.get())
        if r == None:
            error_response = error_response + " Błąd w emailu.\n"
        else:
            email = r.group(0)

        r = re.match(phone_number_regex, self.phone_number_entry.get())
        if r == None:
            error_response = error_response + " Błąd w numerze telefonu.\n"
        else:
            phone_number = r.group(0)

        if error_response == "": # if every entry is correct
            print("=========== wszystko ok ===============")
            print(first_name + " " + last_name + " " + city + " " + email + " " + phone_number)
            db.add_client(first_name, last_name, city, email, phone_number)
            self.window.destroy()
            self.main.show_clients()
        else: # if some entry is not correct
            error_response = "Niepoprawne dane w poszczególnych miejscach:\n\n" + error_response
            print("=========== blad ===============")
            print(error_response)
            messagebox.showerror(title="Błąd", message=error_response, parent=self.window)

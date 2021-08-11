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
        self.window.title("Dodawanie samochodu")
        self.window.iconbitmap(gp.ICON_PATH)
        self.window.configure(bg=gp.BG_COLOR)

        # frame for border look of the main frame
        self.border_view_frame = tk.Frame(self.window, bg=gp.BORDER_COLOR, bd=7)
        self.border_view_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        # main frame
        self.view_frame = tk.Frame(self.border_view_frame, bg=gp.BG_COLOR, bd=5)
        self.view_frame.place(relwidth=1, relheight=1)       

        # label and entry
        self.brand_label = tk.Label(self.view_frame, text="Marka: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.brand_label.place(relx=0.1, rely=0.15, relwidth=0.4, relheight=0.1)

        self.brand_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.brand_entry.place(relx=0.5, rely=0.15, relwidth=0.4, relheight=0.1)

        self.model_label = tk.Label(self.view_frame, text="Model: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.model_label.place(relx=0.1, rely=0.25, relwidth=0.4, relheight=0.1)

        self.model_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.model_entry.place(relx=0.5, rely=0.25, relwidth=0.4, relheight=0.1)

        self.year_label = tk.Label(self.view_frame, text="Rok: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.year_label.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.1)

        self.year_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.year_entry.place(relx=0.5, rely=0.35, relwidth=0.4, relheight=0.1)

        self.fuel_label = tk.Label(self.view_frame, text="Paliwo: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.fuel_label.place(relx=0.1, rely=0.45, relwidth=0.4, relheight=0.1)

        self.fuel_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.fuel_entry.place(relx=0.5, rely=0.45, relwidth=0.4, relheight=0.1)

        self.price_label = tk.Label(self.view_frame, text="Cena: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.price_label.place(relx=0.1, rely=0.55, relwidth=0.4, relheight=0.1)

        self.price_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.price_entry.place(relx=0.5, rely=0.55, relwidth=0.4, relheight=0.1)

        # buttons
        self.submit_button = tk.Button(self.view_frame, text="Dodaj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.add)
        self.submit_button.place(relx=0.2, rely=0.75, relwidth=0.3, relheight=0.1)

        self.cancel_button = tk.Button(self.view_frame, text="Anuluj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.window.destroy)
        self.cancel_button.place(relx=0.5, rely=0.75, relwidth=0.3, relheight=0.1)

    def add(self):
        error_response = ""
        brand_regex = r"[a-zA-Z0-9\-]{2,20}"
        model_regex = r"[a-zA-Z0-9\-]{1,30}"
        year_regex = r"20\d{2}"
        fuel_regex = r"[a-zA-Z0-9\-]{3,20}"
        price_regex = r"\d{2,4}|[1-9]"

        r = re.match(brand_regex, self.brand_entry.get())
        if r == None:
            error_response = error_response + " Błąd w marce.\n"
        else:
            brand = r.group(0)

        r = re.match(model_regex, self.model_entry.get())
        if r == None:
            error_response = error_response + " Błąd w modelu.\n"
        else:
            model = r.group(0)
        
        r = re.match(year_regex, self.year_entry.get())
        if r == None:
            error_response = error_response + " Błąd w roku.\n"
        else:
            year = r.group(0)

        r = re.match(fuel_regex, self.fuel_entry.get())
        if r == None:
            error_response = error_response + " Błąd w paliwie.\n"
        else:
            fuel = r.group(0)

        r = re.match(price_regex, self.price_entry.get())
        if r == None:
            error_response = error_response + " Błąd w cenie.\n"
        else:
            price = r.group(0)

        if error_response == "": # if every entry is correct
            print("=========== wszystko ok ===============")
            print(brand + " " + model + " " + year + " " + fuel + " " + price)
            db.add_car(brand, model, year, fuel, price)
            self.window.destroy()
            self.main.show_cars()
        else: # if some entry is not correct
            error_response = "Niepoprawne dane w poszczególnych miejscach:\n\n" + error_response
            print("=========== blad ===============")
            print(error_response)
            messagebox.showerror(title="Błąd", message=error_response, parent=self.window)

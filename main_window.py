import database as db
import dev as dev
import graphics as gp
import add_car as add_car
import delete_car as delete_car
import rent_car as rent_car
import return_car as return_car
import add_client as add_client

import tkinter as tk
from tkinter import ttk

class Main_Window:
    """
    This class have main window with all the methods
    """
    def __init__(self):
        # main window
        self.main = tk.Tk()
        self.main.title("Wypożyczalnia samochodów")
        self.main.geometry("1300x700")
        self.main.iconbitmap(gp.ICON_PATH)
        self.main.configure(bg=gp.BG_COLOR)

        # frame for top buttons
        self.buttons_frame = tk.Frame(self.main, bg=gp.BORDER_COLOR, bd=5)
        self.buttons_frame.place(relx=0.5, rely=0.05, relwidth=0.8, relheight=0.1, anchor="n")

        # top buttons
        self.button_addcar = tk.Button(self.buttons_frame, text="DODAJ AUTO", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.add_car)
        self.button_addcar.place(relx=0.01, relwidth=0.18, relheight=1)

        self.button_deletecar = tk.Button(self.buttons_frame, text="USUŃ AUTO", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.delete_car)
        self.button_deletecar.place(relx=0.21, relwidth=0.18, relheight=1)

        self.button_rentcar = tk.Button(self.buttons_frame, text="WYNAJMIJ AUTO", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.rent_car)
        self.button_rentcar.place(relx=0.41, relwidth=0.18, relheight=1)

        self.button_returncar = tk.Button(self.buttons_frame, text="ODDAJ AUTO", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.return_car)
        self.button_returncar.place(relx=0.61, relwidth=0.18, relheight=1)

        self.button_addclient = tk.Button(self.buttons_frame, text="DODAJ KLIENTA", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.add_client)
        self.button_addclient.place(relx=0.81, relwidth=0.18, relheight=1)

        # frame for border look of the main frame
        self.border_view_frame = tk.Frame(self.main, bg=gp.BORDER_COLOR, bd=7)
        self.border_view_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.6, anchor="n")

        # main frame
        self.view_frame = tk.Frame(self.border_view_frame, bg=gp.MAIN_FRAME_BG_COLOR, bd=5)
        self.view_frame.place(relwidth=1, relheight=1)

        self.scrollbar = tk.Scrollbar(self.view_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.main_list = ttk.Treeview(self.view_frame, selectmode="browse", yscrollcommand=self.scrollbar.set)
        self.main_list.pack(side="left", fill="both")
        self.scrollbar.config( command = self.main_list.yview )
        # default view shows clients
        self.show_clients()
        self.main_list_type = "clients"

        # frame for bottom button
        self.view_buttons = tk.Frame(self.main, bg=gp.BORDER_COLOR, bd=5)
        self.view_buttons.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.1, anchor="n")

        # bottom button
        self.button_seeclients = tk.Button(self.view_buttons, text="WYŚWIETL KLIENTÓW", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.show_clients)
        self.button_seeclients.place(relx=0.025, relwidth=0.3, relheight=1)

        self.button_seecars = tk.Button(self.view_buttons, text="WYŚWIETL AUTA", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.show_cars)
        self.button_seecars.place(relx=0.35, relwidth=0.3, relheight=1)

        self.button_seerents = tk.Button(self.view_buttons, text="WYŚWIETL WYPOŻYCZENIA", font=gp.FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, bd=4, command=self.show_rents)
        self.button_seerents.place(relx=0.675, relwidth=0.3, relheight=1)

    def start(self):
        self.main.mainloop()

    def show_clients(self):
        self.scrollbar.destroy()
        self.scrollbar = tk.Scrollbar(self.view_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.main_list.destroy()
        self.main_list_type = "clients"
        self.main_list = ttk.Treeview(self.view_frame, selectmode="browse", yscrollcommand=self.scrollbar.set)

        self.main_list["columns"]=("first_name", "last_name", "city", "email", "phone_number")
        self.main_list.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.main_list.column("first_name", width=190, minwidth=70, stretch=tk.NO)
        self.main_list.column("last_name", width=190, minwidth=70, stretch=tk.NO)
        self.main_list.column("city", width=160, minwidth=70, stretch=tk.NO)
        self.main_list.column("email", width=220, minwidth=120, stretch=tk.NO)
        self.main_list.column("phone_number", width=180, minwidth=90, stretch=tk.NO)

        self.main_list.heading("#0", text="Id", anchor=tk.W)
        self.main_list.heading("first_name", text="Imie", anchor=tk.W)
        self.main_list.heading("last_name", text="Nazwisko", anchor=tk.W)
        self.main_list.heading("city", text="Miasto", anchor=tk.W)
        self.main_list.heading("email", text="E-mail", anchor=tk.W)
        self.main_list.heading("phone_number", text="Nr telefonu", anchor=tk.W)

        listac = db.get_clients()
        for e in listac:
            self.main_list.insert("", "end", iid=e.id, text=e.id, values=(e.first_name, e.last_name, e.city, e.email, e.phone_number))

        self.main_list.pack(side="left", fill="both")
        self.scrollbar.config( command = self.main_list.yview )

    def show_cars(self):
        self.scrollbar.destroy()
        self.scrollbar = tk.Scrollbar(self.view_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.main_list.destroy()
        self.main_list_type = "cars"
        self.main_list = ttk.Treeview(self.view_frame, selectmode="browse", yscrollcommand=self.scrollbar.set)

        self.main_list["columns"]=("brand", "model", "year", "fuel", "price", "start_date", "end_date", "client")
        self.main_list.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.main_list.column("brand", width=140, minwidth=70, stretch=tk.NO)
        self.main_list.column("model", width=150, minwidth=70, stretch=tk.NO)
        self.main_list.column("year", width=60, minwidth=30, stretch=tk.NO)
        self.main_list.column("fuel", width=120, minwidth=60, stretch=tk.NO)
        self.main_list.column("price", width=50, minwidth=40, stretch=tk.NO)
        self.main_list.column("start_date", width=180, minwidth=150, stretch=tk.NO)
        self.main_list.column("end_date", width=180, minwidth=150, stretch=tk.NO)
        self.main_list.column("client", width=60, minwidth=50, stretch=tk.NO)

        self.main_list.heading("#0", text="Id", anchor=tk.W)
        self.main_list.heading("brand", text="Marka", anchor=tk.W)
        self.main_list.heading("model", text="Model", anchor=tk.W)
        self.main_list.heading("year", text="Rok", anchor=tk.W)
        self.main_list.heading("fuel", text="Paliwo", anchor=tk.W)
        self.main_list.heading("price", text="Cena", anchor=tk.W)
        self.main_list.heading("start_date", text="Data poczatkowa", anchor=tk.W)
        self.main_list.heading("end_date", text="Data koncowa", anchor=tk.W)
        self.main_list.heading("client", text="Klient", anchor=tk.W)

        listac = db.get_cars()
        for e in listac:
            if e.start_date == None:
                e.start_date = "----"
            if e.end_date == None:
                e.end_date = "----"
            if e.client == None:
                e.client = "----"
            self.main_list.insert("", "end", iid=e.id, text=e.id, values=(e.brand, e.model, e.year, e.fuel, e.price, e.start_date, e.end_date, e.client))

        self.main_list.pack(side="left", fill="both")
        self.scrollbar.config( command = self.main_list.yview )

    def show_rents(self):
        self.scrollbar.destroy()
        self.scrollbar = tk.Scrollbar(self.view_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        self.main_list.destroy()
        self.main_list_type = "rents"
        self.main_list = ttk.Treeview(self.view_frame, selectmode="browse", yscrollcommand=self.scrollbar.set)

        self.main_list["columns"]=("first_name/brand", "last_name/model", "city/year", "email/fuel", "phone_number/price", "start_date", "end_date")
        self.main_list.column("#0", width=70, minwidth=70, stretch=tk.NO)
        self.main_list.column("first_name/brand", width=110, minwidth=90, stretch=tk.NO)
        self.main_list.column("last_name/model", width=130, minwidth=100, stretch=tk.NO)
        self.main_list.column("city/year", width=90, minwidth=70, stretch=tk.NO)
        self.main_list.column("email/fuel", width=170, minwidth=120, stretch=tk.NO)
        self.main_list.column("phone_number/price", width=120, minwidth=120, stretch=tk.NO)
        self.main_list.column("start_date", width=150, minwidth=150, stretch=tk.NO)
        self.main_list.column("end_date", width=150, minwidth=150, stretch=tk.NO)

        self.main_list.heading("#0", text="Id", anchor=tk.W)
        self.main_list.heading("first_name/brand", text="Imie / Marka", anchor=tk.W)
        self.main_list.heading("last_name/model", text="Nazwisko / Model", anchor=tk.W)
        self.main_list.heading("city/year", text="Miasto / Rok", anchor=tk.W)
        self.main_list.heading("email/fuel", text="E-mail / Paliwo", anchor=tk.W)
        self.main_list.heading("phone_number/price", text="Nr telefonu / Cena", anchor=tk.W)
        self.main_list.heading("start_date", text=" / Data poczatkowa", anchor=tk.W)
        self.main_list.heading("end_date", text=" / Data koncowa", anchor=tk.W)

        listac = db.get_clients_with_cars()
        tab = []
        i = 0
        for e in listac:
            tab.append(self.main_list.insert("", "end", iid="c"+str(e.id), text=e.id, values=(e.first_name, e.last_name, e.city, e.email, e.phone_number)))
            for c in e.car:
                self.main_list.insert(tab[i], "end", iid=c.id, text=c.id, values=(c.brand, c.model, c.year, c.fuel, c.price, c.start_date, c.end_date, c.client))
            i = i + 1

        self.main_list.pack(side="left", fill="both")
        self.scrollbar.config( command = self.main_list.yview )

    def add_car(self):
        add_car.Window(self)

    def delete_car(self):
        delete_car.Window(self)

    def rent_car(self):
        rent_car.Window(self)

    def return_car(self):
        return_car.Window(self)

    def add_client(self):
        add_client.Window(self)
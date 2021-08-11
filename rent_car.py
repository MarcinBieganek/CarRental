import database as db
import dev as dev
import graphics as gp

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import date, datetime, timedelta
import re

class Window:
    def __init__(self, main):
        self.main = main
        self.main.show_cars()
        self.window = tk.Toplevel()
        self.window.geometry("700x550")
        self.window.title("Wypożyczanie samochodu")
        self.window.iconbitmap(gp.ICON_PATH)
        self.window.configure(bg=gp.BG_COLOR)

        # frame for border look of the main frame
        self.border_view_frame = tk.Frame(self.window, bg=gp.BORDER_COLOR, bd=7)
        self.border_view_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        # main frame
        self.view_frame = tk.Frame(self.border_view_frame, bg=gp.BG_COLOR, bd=5)
        self.view_frame.place(relwidth=1, relheight=1)

        # labels, buttons and variables
        self.car_pick_info_label = tk.Label(self.view_frame, text="Proszę zaznaczyć samochód do wypożyczenia z listy\n w głównym oknie i potwierdzić przyciskiem 'Wybierz' poniżej.", font=gp.SMALL_FONT, bg=gp.BG_COLOR)
        self.car_pick_info_label.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.15)

        self.car_pick_button = tk.Button(self.view_frame, text="Wybierz", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.car_pick)
        self.car_pick_button.place(relx=0.2, rely=0.17, relwidth=0.6, relheight=0.1)

        self.car_id = ()
        self.car_pick_ok = False

        self.client_pick_info_label = tk.Label(self.view_frame, text="Proszę zaznaczyć klienta z listy w głównym oknie\n i potwierdzić przyciskiem 'Wybierz' poniżej.", font=gp.SMALL_FONT, bg=gp.BG_COLOR)
        self.client_pick_info_label.place(relx=0.1, rely=0.28, relwidth=0.8, relheight=0.15)

        self.client_pick_button = tk.Button(self.view_frame, text="Wybierz", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.client_pick)
        self.client_pick_button.place(relx=0.2, rely=0.44, relwidth=0.6, relheight=0.1)

        self.client_id = ()
        self.client_pick_ok = False

        # labels and entries
        self.start_date_label = tk.Label(self.view_frame, text="Data początkowa: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.start_date_label.place(relx=0.1, rely=0.60, relwidth=0.4, relheight=0.1)

        start_date_proposal = datetime.today().replace(microsecond=0)
        self.start_date_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.start_date_entry.insert(0, start_date_proposal)
        self.start_date_entry.place(relx=0.5, rely=0.60, relwidth=0.4, relheight=0.1)

        self.end_date_label = tk.Label(self.view_frame, text="Data końcowa: ", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR)
        self.end_date_label.place(relx=0.1, rely=0.70, relwidth=0.4, relheight=0.1)

        self.end_date_entry = tk.Entry(self.view_frame, font=gp.SMALL_FONT)
        self.end_date_entry.insert(0, "np. 2020-02-14 (rrrr-mm-dd)")
        self.end_date_entry.place(relx=0.5, rely=0.70, relwidth=0.4, relheight=0.1)

        # bottom buttons
        self.rent_button = tk.Button(self.view_frame, text="Wypożycz", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.rent)
        self.rent_button.place(relx=0.2, rely=0.86, relwidth=0.3, relheight=0.1)

        self.cancel_button = tk.Button(self.view_frame, text="Anuluj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.window.destroy)
        self.cancel_button.place(relx=0.5, rely=0.86, relwidth=0.3, relheight=0.1)

    def car_pick(self):
        error_response = ""
        try:
            self.car_id = self.main.main_list.selection()
        except:
            error_response = "Proszę wybrać samochód do wynajęcia w głównym oknie.\n"
            self.main.show_cars()
        else:
            if self.main.main_list_type == "cars":
                if self.car_id == (): # if car was not selected
                    error_response = "Proszę wybrać samochód do wynajęcia w głównym oknie.\n"
                else: # if car was selected
                    self.car_pick_ok = True
                    self.car_id = self.car_id[0]
                    print("====================== auto id:   " + str(self.car_id) + "        ===================")
                    self.main.show_clients()
            else:
                error_response = "Proszę wybrać samochód do usunięcia w głównym oknie.\n"
                self.main.show_cars()
        finally:
            if error_response != "": # if some error appeard
                print("========  " + error_response)
                messagebox.showerror(title="Błąd", message=error_response, parent=self.window)

    def client_pick(self):
        error_response = ""
        try:
            self.client_id = self.main.main_list.selection()
        except:
            error_response = "Proszę wybrać klienta w głównym oknie.\n"
            self.main.show_clients()
        else:
            if self.main.main_list_type == "clients":
                if self.client_id == (): # if client was not selected
                    error_response = "Proszę wybrać klienta w głównym oknie.\n"
                else: # if client was selected
                    self.client_pick_ok = True
                    self.client_id = self.client_id[0]
                    print("====================== klient id:   " + str(self.client_id) + "        ===================")
            else:
                error_response = "Proszę wybrać klienta w głównym oknie.\n"
                self.main.show_clients()
        finally:
            if error_response != "": # if some error appeard
                print("========  " + error_response)
                messagebox.showerror(title="Błąd", message=error_response, parent=self.window)

    def rent(self):
        error_response = ""
        start_date_regex = r"20\d{2}-(0[1-9]|1[0-2])-(3[0-1]|[1-2]\d|0[1-9]) (2[0-4]|[0-1]\d):[0-5]\d:[0-5]\d(\.\d{1,6})?"
        end_date_regex = r"20\d{2}-(0[1-9]|1[0-2])-(3[0-1]|[1-2]\d|0[1-9])" # we do only take end date whithout time
        # car pick check
        if self.car_pick_ok == False:
            error_response = "Proszę wybrać samochód do wynajęcia w głównym oknie.\n"
        # client pick check
        if self.client_pick_ok == False:
            error_response = error_response + "Proszę wybrać klienta w głównym oknie.\n"
        # start_date check
        r = re.match(start_date_regex, self.start_date_entry.get())
        if r == None:
            error_response = error_response + "Błąd w dacie początkowej.\n"
        else:
            start_date = datetime.fromisoformat(r.group(0))
            hour = timedelta(hours=1)
            now = datetime.today()
            if now - start_date > hour:
                error_response = error_response + "Data początkowa nie może być wcześniejsza o ponad godzinę od obecnej daty.\n"
            if start_date - now > hour:
                error_response = error_response + "Data początkowa nie może być późniejsza o ponad godzinę od obecnej daty.\n"

        # end_date check
        r = re.match(end_date_regex, self.end_date_entry.get())
        if r == None:
            error_response = error_response + "Błąd w dacie końcowej.\n"
        else:
            end_date = datetime.fromisoformat(r.group(0) + " 23:59:59")
            now = datetime.today()
            if end_date < now:
                error_response = error_response + "Data końcowa nie może być wcześniejsza od obecnej daty.\n"
        
        if error_response == "": # if all input is good
            period = end_date - start_date
            period = period.days
            # summary preperation
            car = db.get_car(self.car_id)
            price = car.price
            cost = period * price
            summary_message = "Podsumowanie:\n\n"
            summary_message = summary_message + "Data początkowa: " + str(start_date) + "\n"
            summary_message = summary_message + "Data końcowa:      " + str(end_date) + "\n"
            summary_message = summary_message + "Ilość dni:  " + str(period) + "\n"
            summary_message = summary_message + "Cena:       " + str(price) + " PLN/dzień" + "\n"
            summary_message = summary_message + "Koszt:      " + str(cost) + " PLN" + "\n"

            error_response = db.rent_car(self.car_id, self.client_id, start_date, end_date)
            
        if error_response != "": # if some error appeard
            print("========  " + error_response)
            messagebox.showerror(title="Błąd", message=error_response, parent=self.window)
        else:
            self.window.destroy()
            self.main.show_rents()
            messagebox.showinfo(title="Podsumowanie", message=summary_message, parent=self.main.main)
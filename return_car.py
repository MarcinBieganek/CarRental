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
        self.main.show_rents()
        self.window = tk.Toplevel()
        self.window.geometry("600x400")
        self.window.title("Oddawanie samochodu")
        self.window.iconbitmap(gp.ICON_PATH)
        self.window.configure(bg=gp.BG_COLOR)

        # frame for border look of the main frame
        self.border_view_frame = tk.Frame(self.window, bg=gp.BORDER_COLOR, bd=7)
        self.border_view_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        # main frame
        self.view_frame = tk.Frame(self.border_view_frame, bg=gp.BG_COLOR, bd=5)
        self.view_frame.place(relwidth=1, relheight=1)

        # label
        self.car_pick_info_label = tk.Label(self.view_frame, text="Proszę zaznaczyć samochód do oddania\n z listy w głównym oknie i potwierdzić\n przyciskiem 'Oddaj' poniżej.", font=gp.SMALL_FONT, bg=gp.BG_COLOR)
        self.car_pick_info_label.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.2)

        # button
        self.return_button = tk.Button(self.view_frame, text="Oddaj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.creturn)
        self.return_button.place(relx=0.2, rely=0.6, relwidth=0.3, relheight=0.15)

        self.cancel_button = tk.Button(self.view_frame, text="Anuluj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.window.destroy)
        self.cancel_button.place(relx=0.5, rely=0.6, relwidth=0.3, relheight=0.15)

    def creturn(self):
        error_response = ""
        try:
            car_id = self.main.main_list.selection()
        except:
            error_response = "Proszę wybrać samochód do oddania w głównym oknie.\n"
            self.main.show_rents()
        else:
            if self.main.main_list_type == "rents":
                if car_id == (): # if car was not selected
                    error_response = "Proszę wybrać samochód do oddania w głównym oknie.\n"
                elif car_id[0][0] == "c": # if client was selected
                    error_response = "Proszę wybrać samochód, a nie klienta, do oddania w głównym oknie.\n"
                else: # if car was selected
                    car_id = car_id[0]
                    # summary preperation
                    car = db.get_car(car_id)
                    end_date = car.end_date
                    today = datetime.today().replace(microsecond=0)
                    difference = (today - end_date).days
                    summary_message = "Podsumowanie:\n\n"
                    summary_message = summary_message + "Data końcowa:      " + str(end_date) + "\n"
                    summary_message = summary_message + "Dzisiejsza data:      " + str(today) + "\n"
                    if difference <= 0:
                        summary_message = summary_message + "Oddano w planowanym terminie, żadna dopłata nie jest wymagana.\n"
                    else:
                        price = car.price
                        cost = price * difference
                        summary_message = summary_message + "Oddano " + str(difference) + " dni po planowanym terminie. \nDopłata wynosi: " + str(cost) + " PLN. \n"

                    error_response = db.return_car(car_id)
            else:
                error_response = "Proszę wybrać samochód do oddania w głównym oknie.\n"
                self.main.show_rents()
        finally:
            if error_response != "": # if some error appeard
                print("========  " + error_response)
                messagebox.showerror(title="Błąd", message=error_response, parent=self.window)
            else:
                self.window.destroy()
                self.main.show_rents()
                messagebox.showinfo(title="Podsumowanie", message=summary_message, parent=self.main.main)
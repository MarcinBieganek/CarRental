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
        self.window.geometry("600x400")
        self.window.title("Usuwanie samochodu")
        self.window.iconbitmap(gp.ICON_PATH)
        self.window.configure(bg=gp.BG_COLOR)

        # frame for border look of the main frame
        self.border_view_frame = tk.Frame(self.window, bg=gp.BORDER_COLOR, bd=7)
        self.border_view_frame.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.8, anchor="n")

        # main frame
        self.view_frame = tk.Frame(self.border_view_frame, bg=gp.BG_COLOR, bd=5)
        self.view_frame.place(relwidth=1, relheight=1)

        # label
        self.car_pick_info_label = tk.Label(self.view_frame, text="Proszę zaznaczyć samochód do usunięcia\n z listy w głównym oknie i potwierdzić\n przyciskiem 'Usuń' poniżej.", font=gp.SMALL_FONT, bg=gp.BG_COLOR)
        self.car_pick_info_label.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.2)

        # buttons
        self.delete_button = tk.Button(self.view_frame, text="Usuń", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.delete)
        self.delete_button.place(relx=0.2, rely=0.6, relwidth=0.3, relheight=0.15)

        self.cancel_button = tk.Button(self.view_frame, text="Anuluj", font=gp.SMALL_FONT, bg=gp.BUTTON_COLOR, activebackground=gp.BUTTON_COLOR, command=self.window.destroy)
        self.cancel_button.place(relx=0.5, rely=0.6, relwidth=0.3, relheight=0.15)  

    def delete(self):
        error_response = ""
        try:
            car_id = self.main.main_list.selection()
        except:
            error_response = "Proszę wybrać samochód do usunięcia w głównym oknie.\n"
            self.main.show_cars()
        else:
            if self.main.main_list_type == "cars":
                if car_id == (): # if car was not selected
                    error_response = "Proszę wybrać samochód do usunięcia w głównym oknie.\n"
                else: # if car was selected
                    car_id = car_id[0]
                    error_response = db.delete_car(car_id)
            else:
                error_response = "Proszę wybrać samochód do usunięcia w głównym oknie.\n"
                self.main.show_cars()
        finally:
            if error_response != "": # if some error appeard
                print("===============  " + error_response)
                messagebox.showerror(title="Błąd", message=error_response, parent=self.window)
            else:
                self.window.destroy()
                self.main.show_cars()

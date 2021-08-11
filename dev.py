from datetime import date, datetime, timedelta
from tabulate import tabulate
import database as db

def show():
    listak = db.get_cars()
    wynikk = []

    for e in listak:
        s = [e.id, e.brand, e.model, e.year, e.fuel, e.price, e.start_date, e.end_date, e.client]
        wynikk.append(s)

    print(" --- Tabela aut:   ---")
    print(tabulate(wynikk, headers=["Id", "Brand", "Model", "Year", "Fuel", "Price", "Start Date", "End Date", "Client"], tablefmt="github"))

    listaz = db.get_clients()
    wynikz = []

    for e in listaz:
        s = [e.id, e.first_name, e.last_name, e.city, e.email, e.phone_number]
        wynikz.append(s)

    print(" --- Tabela klientow:   ---")
    print(tabulate(wynikz, headers=["Id", "First Name", "Last Name", "City", "Email", "Phone Number"], tablefmt="github"))

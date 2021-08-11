from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, relationship, Load, undefer, eagerload
from datetime import date, datetime, timedelta

# Data base settings
Base = declarative_base()
engine = create_engine("sqlite:///baza.db", echo=True)

class Car(Base):
    __tablename__ = "Car"
    id = Column(Integer, primary_key=True)
    brand = Column(String(20), nullable=False)
    model = Column(String(30), nullable=False)
    year = Column(Integer, nullable=False)
    fuel = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    client = Column(Integer, ForeignKey("Client.id"))

class Client(Base):
    __tablename__ = "Client"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    city = Column(String(45), nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String(10), nullable=False)

    car = relationship("Car")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create():
    s = Session()  
    car1 = Car(brand="Ford", model="Focus", year=2017 , fuel="benzyna", price=40)
    car2 = Car(brand="Ford", model="Mondeo", year=2019 , fuel="benzyna", price=65)
    car3 = Car(brand="Volksvagen", model="Polo", year=2018 , fuel="diesel", price=45)
    client1 = Client(first_name="Marek", last_name="Kowalski", city="Wrocław", email="mkowalski@gmail.com", phone_number="666123092")
    client2 = Client(first_name="Tomek", last_name="Bąk", city="Wrocław", email="TomekBak123@wp.pl", phone_number="901788292")
    client3 = Client(first_name="Edward", last_name="Zieliński", city="Opole", email="edwardz1234@gmail.com", phone_number="551892771")
    
    car3.start_date = datetime.today()
    car3.end_date = date.fromisoformat("2020-01-29")
    client2.car = [car3]

    s.add(car1)
    s.add(car2)
    s.add(car3)
    s.add(client1)
    s.add(client2)
    s.add(client3)
    s.commit()
    s.close()


def add_car(brand, model, year, fuel, price):
    s = Session()
    c = Car(brand=brand, model=model, year=year, fuel=fuel, price=price)
    s.add(c)
    s.commit()
    s.close()

def add_client(first_name, last_name, city, email, phone_number):
    s = Session()
    c = Client(first_name=first_name, last_name=last_name, city=city, email=email, phone_number=phone_number)
    s.add(c)
    s.commit()
    s.close()

def delete_car(id):
    error_response = ""
    s = Session()
    car = s.query(Car).filter(Car.id == id).first()

    if car == None: # if selected car is not in database
       error_response = "Wystąpił błąd, proszę spróbować ponownie.\n"
    else: # if selected car is in database
        if car.client == None: # if selected car is not rented
            print("=============== Delete === " + str(car.id) + "  =====")
            s.delete(car)
            s.commit()
        else: # if selected car is rented
            error_response = "Nie można usnąć samochodu ponieważ jest wypożyczony.\n"

    s.close()
    return error_response

def rent_car(car_id, client_id, start_date, end_date):
    error_response = ""
    s = Session()
    car = s.query(Car).filter(Car.id == int(car_id)).first()

    if car == None: # if selected car is not in database
        error_response = "Wystąpił błąd, proszę spróbować ponownie.\n"
    else: # if selected car is in database
        if car.client == None: # if selected car is not rented
            client = s.query(Client).filter(Client.id == int(client_id)).first()
            if client == None: # if selected car is not in database
                error_response = "Wystąpił błąd, proszę spróbować ponownie.\n"
            else:
                print("=============== Rent ===  " + str(car.id) + "   =====")

                car.start_date = start_date
                car.end_date = end_date
                client.car.append(car)
                s.commit()
        else: # if selected car is rented
            error_response = "Nie można wypożyczyć samochodu ponieważ jest wypożyczony.\n"

    s.close()
    return error_response

def return_car(car_id):
    error_response = ""
    s = Session()
    car = s.query(Car).filter(Car.id == car_id).first()

    if car == None: # if selected car is not in database
        error_response = "Wystąpił błąd, proszę spróbować ponownie.\n"
    else: # if selected car is in database
        if car.client == None: # if selected car is not rented
            error_response = "Nie można oddać samochodu ponieważ nie jest wypożyczony.\n"
        else: # if selected car is rented
            client = s.query(Client).filter(Client.id == car.client).first()
            if client == None:
                error_response = "Wystąpił błąd, proszę spróbować ponownie.\n"
            else:
                print("=============== Return ===  " + str(car.id) + "   =====")

                car.start_date = None
                car.end_date = None
                client.car.remove(car)
                s.commit()

    s.close()
    return error_response

def get_car(id):
    s = Session()
    car = s.query(Car).options(undefer("*")).filter(Car.id == id).first()
    s.close()
    return car

def get_cars():
    s = Session()
    cars = s.query(Car).options(undefer("*")).all()
    s.close()
    return cars

def get_clients():
    s = Session()
    clients = s.query(Client).options(undefer("*")).all()
    s.close()
    return clients

def get_clients_with_cars():
    s = Session()
    clients = s.query(Client).options(undefer("*"), eagerload(Client.car)).all()
    s.close()
    return clients
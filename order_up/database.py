from dotenv import load_dotenv
load_dotenv()

from app import app, db
from app.models import Employee, MenuItemType, Menu, MenuItem, Table


with app.app_context():
  db.drop_all()
  db.create_all()

  names = ['Margot', 'Billy', 'Sara', 'Penny', 'Paul']
  for i in range(len(names)):
    db.session.add(Employee(name = names[i], employee_number = int(i + 100), password = "password"))

  beverages = MenuItemType(name = "Beverages")
  entrees = MenuItemType(name = "Entrees")
  sides = MenuItemType(name = "Sides")

  dinner = Menu(name = "Dinner")

  drp = MenuItem(name = "Dr. Pepper", price = 1.0, type = beverages, menu = dinner)
  tea = MenuItem(name = "Tea", price = 2.98, type = beverages, menu = dinner)
  lingonberry_soda = MenuItem(name = "Lingonberry Soda", price = 4.00, type = beverages, menu = dinner)
  fries = MenuItem(name = "French fries", price = 3.50, type = sides, menu = dinner)
  deep_fired_onions = MenuItem(name = "Deep Fried Onions", price = 5.1, type = sides, menu = dinner)
  jambalaya = MenuItem(name = "Jambalaya", price = 21.98, type = entrees, menu = dinner)
  chicken_kiev = MenuItem(name = "Chicken Kiev", price = 12.99, type = entrees, menu = dinner)
  eggplant_parmesan = MenuItem(name = "Eggplant Parmesan", price = 13.99, type = entrees, menu = dinner)

  for i in range(10):
    db.session.add(Table(number = i + 1, capacity = (i + 1) * 10))

  db.session.add(dinner)
  db.session.commit()

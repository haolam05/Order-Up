from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from .. import db
from ..forms import TableAssignmentForm, MenuItemAssignmentForm
from ..models import Table, Order, Employee, MenuItem, MenuItemType, OrderDetail

bp = Blueprint("orders", __name__, url_prefix="")


@bp.route("/")
@login_required
def index():
  form = TableAssignmentForm()


  """ Display tables <option> """
  tables = Table.query.order_by(Table.number).all()
  open_orders = Order.query.filter(Order.finished == False)
  busy_table_ids = [order.table_id for order in open_orders]
  open_tables = [table for table in tables if table.id not in busy_table_ids]
  form.tables.choices = [(table.id, f"Table {table.number}") for table in open_tables]


  """ Display servers <option> """
  servers = Employee.query.all()
  form.servers.choices = [(server.id, f"{server.name} - {server.employee_number}") for server in servers]


  """ Display menu's items <option> """
  items = MenuItem.query.join(MenuItemType).order_by(MenuItemType.name, MenuItem.name)
  item_to_type = { item.id: item.type.name for item in items }

  form_2 = MenuItemAssignmentForm()
  form_2.menu_item_ids.choices = [(item.id, f"{item_to_type[item.id]} - {item.name} - ${item.price}") for item in MenuItem.query.order_by(MenuItem.menu_type_id).all()]


  """ Calculating total cost of food for each table """
  table_to_orders = {}
  busy_table_orders = Order.query.filter(Order.table_id.in_(busy_table_ids)).all()
  for order in busy_table_orders:
    if order.table_id in table_to_orders:
      table_to_orders[order.table_id].append(order.id)
    else:
      table_to_orders[order.table_id] = [order.id]

  table_to_sum = {}
  for table, orders in table_to_orders.items():
    for order_id in orders:
      order_details = OrderDetail.query.filter(OrderDetail.order_id == order_id).all()
      item_to_quantity = {}
      for order_detail in order_details:
        if order_detail.menu_item_id in item_to_quantity:
          item_to_quantity[order_detail.menu_item_id] += 1
        else:
          item_to_quantity[order_detail.menu_item_id] = 1
      menu_item_ids = item_to_quantity.keys()
      menu_items = MenuItem.query.filter(MenuItem.id.in_(menu_item_ids)).all()
      for menu_item in menu_items:
        if table in table_to_sum:
          table_to_sum[table] += (menu_item.price) * item_to_quantity[menu_item.id]
        else:
          table_to_sum[table] = (menu_item.price) * item_to_quantity[menu_item.id]

  return render_template("orders.html", form = form, orders = open_orders.all(), form_2 = form_2, table_to_sum = table_to_sum)


@bp.route("/tables/assign", methods=['POST'])
@login_required
def assign_table():
  db.session.add(Order(employee_id = request.form['servers'], table_id = request.form['tables'], finished = False))
  db.session.commit()
  return redirect("/")


@bp.route("/tables/close/<int:order_id>")
@login_required
def close_table(order_id):
  order = Order.query.get(order_id)
  order.finished = True
  order_details = OrderDetail.query.filter(OrderDetail.order_id == order_id).all()
  print(order_details, order_id)
  for order_detail in order_details:
    db.session.delete(order_detail)
  db.session.commit()
  return redirect("/")


@bp.route("/tables/add_to_order/<int:order_id>", methods=['POST'])
@login_required
def add_to_order(order_id):
  menu_item_ids = [int(id) for id in request.form.getlist('menu_item_ids')]
  for menu_item_id in menu_item_ids:
    db.session.add(OrderDetail(menu_item_id = menu_item_id, order_id = order_id))
    db.session.commit()
  return redirect("/")

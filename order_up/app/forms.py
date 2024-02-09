from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
  employee_number = StringField("Employee number", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")


class TableAssignmentForm(FlaskForm):
  tables = SelectField("Tables", coerce = int)
  servers = SelectField("Servers", coerce = int)
  assign = SubmitField("Assign")


class MenuItemAssignmentForm(FlaskForm):
  menu_item_ids = SelectMultipleField("Menu items", coerce = int)

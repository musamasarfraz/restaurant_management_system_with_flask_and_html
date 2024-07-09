from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    submit = SubmitField('Add Item')

class OrderForm(FlaskForm):
    items = TextAreaField('Items', validators=[DataRequired()])
    total_price = FloatField('Total Price', validators=[DataRequired()])
    submit = SubmitField('Place Order')

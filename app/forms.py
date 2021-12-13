from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, PasswordField,SubmitField,TextField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
    username= StringField("username",validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    submit= SubmitField("Sign in")
class RegisterForm(FlaskForm):
    email= StringField("email",validators=[DataRequired()])
    username= StringField("username",validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    confirm=PasswordField("confirm",validators=[DataRequired()])
    submit= SubmitField("Register")
class BookForm(FlaskForm):
    bookname=StringField("bookname",validators=[DataRequired()])
    author=StringField("author",validators=[DataRequired()])
    img=StringField("img",validators=[DataRequired()])
    price= StringField("price",validators=[DataRequired()])
    submit= SubmitField("Save")
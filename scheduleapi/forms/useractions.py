# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Required, Optional, Length, Email


class Login(Form):
    username = StringField('Username', validators=[
        Required(message='Please pick a username'),
        Length(min=2, max=25,
            message='Username needs to be between 2 and 25 characters'
        )
    ])
    password = PasswordField('Password', validators=[
        Required(message='Please choose a password'),
        Length(min=5, max=50,
            message='Password needs to be between 5 and 50 characters'
        )
    ])
    remember_me = BooleanField('Remember me?', default = False)

class Register(Form):
    username = StringField('Username', validators=[
        Required(message='Please type your username')
    ])
    password = PasswordField('Password', validators=[
        Required(message='Please type your password')
    ])
    email = StringField('Email', validators=[
        Email(message='Email is not valid'), Optional()
    ])

# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Email, Length
import time


class CommentForm(FlaskForm):
    """
    Formulario de contacto
    """
    username = StringField('Su nombre', validators=[InputRequired()])
    email = StringField('Su email', validators=[
        InputRequired(), Email(message='Ingrese un Email valido')])
    message = TextAreaField('Su mensaje', validators=[InputRequired()])
    submit = SubmitField('Enviar mensaje')
    now = time.strftime("%Y/%m/%d")


class LoginForm(FlaskForm):
    """
    Formulario para Login
    """
    username = StringField('Nombre de Usuario',
                           validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Contrasena',
                             validators=[InputRequired(),
                                         Length(min=8, max=80)])
    submit = SubmitField('Ingresar')

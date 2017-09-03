# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from flask_mail import Message
from werkzeug.security import check_password_hash  # generate_password_hash,
from flask_login import login_user, login_required, logout_user, current_user

from app import app, db, mail, connectiondb
from .models import Comentario, User
from .forms import CommentForm, LoginForm


# inicio o home
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():

    form = CommentForm()

    if request.method == 'POST' and form.validate_on_submit():
        comentario = Comentario(
            nombre=form.username.data,
            email=form.email.data,
            mensaje=form.message.data,
            fecha_creacion=form.now)

        db.session.add(comentario)
        db.session.commit()

        # Se envia correo de aviso cuando hay un nuevo mensaje
        msg = Message(
            'Nuevo mensaje',
            recipients=['mmesa_@hotmail.com'])

        msg.body = "Tiene un nuevo mensaje"
        mail.send(msg)

    else:
        pass

    return render_template('index.html', form=form)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

        return 'Nombre de usuario o Contraseña invalidos!'

    return render_template('login.html', form=form)


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# Dashobard
@app.route('/dashboard')
@login_required
def dashboard():
    cursor = connectiondb.cursor()
    sql = "SELECT * FROM comentario ORDER BY id DESC"
    cursor.execute(sql)
    comentarios = cursor.fetchall()

    return render_template('dashboard.html',
                           name=current_user.username,
                           form=comentarios)

    cursor.close()


# Mensajes
@app.route('/dashboard/mensajes/<id_mensaje>')
@login_required
def mensajes(id_mensaje):
    cursor = connectiondb.cursor()
    sql = "SELECT * FROM comentario WHERE id = '%s'" % id_mensaje
    cursor.execute(sql)
    mensaje = cursor.fetchall()

    return render_template('messages.html', form=mensaje)

    cursor.close()


# Parametros
@app.route('/parametros', methods=['GET', 'POST'])
@login_required
def parametros():
    pass

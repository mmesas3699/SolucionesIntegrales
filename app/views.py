# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify
from flask_mail import Message
from werkzeug.security import check_password_hash  # generate_password_hash,
from flask_login import login_user, login_required, logout_user, current_user

from app import app, db, mail, connectiondb
from .models import Comentario, User
from .forms import CommentForm, LoginForm, FormParametrosFactura


# ............ Controladores .................

def generar_numero_factura():
    """ Genera los números de factura """
    cursor_fac = connectiondb.cursor()
    cursor_param = connectiondb.cursor()
    sql_select_fac = """SELECT num_factura
                        FROM Factura
                        ORDER BY num_factura DESC LIMIT 1;"""
    sql_select_param = """SELECT num_fac_ini, num_fac_fin
                          FROM ParametrosFactura;"""

    cursor_fac.execute(sql_select_fac)
    resultado_fac = cursor_fac.fetchall()
    cursor_fac.close()
    cursor_param.execute(sql_select_param)
    resultado_param = cursor_param.fetchall()
    cursor_param.close()

    if len(resultado_fac) == 0:
        if len(resultado_param) == 0:
            return "Falta capturar los consecutivos de las facturas"
        else:
            numero_factura = resultado_param[0]['num_fac_ini']
            return str(numero_factura)
    elif resultado_fac[0]['num_factura'] > resultado_param[0]['num_fac_fin']:
        return "Debe actualizar el consecutivo de las facturas"
    else:
        numero_factura = resultado_fac[0]['num_factura'] + 1
        return str(numero_factura)

    connectiondb.close()


# ................ Vistas ...................

# Inicio o Home
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """ Renderiza el home """
    form = CommentForm()

    return render_template('index.html', form=form)


@app.route('/procesa_mensaje_contacto', methods=['POST'])
def procesa_mensaje_contacto():
    """ Procesa el formulario de contacto """
    form = CommentForm()
    username = request.form['username']
    email = request.form['email']
    mensaje = request.form['message']

    if request.method == 'POST':
        comentario = Comentario(nombre=username,
                                email=email,
                                mensaje=mensaje,
                                fecha_creacion=form.now)

        db.session.add(comentario)
        db.session.commit()

        # Despúes de guardar el mensaje en la base de datos se envia un correo
        # avisando al administrador del nuevo mensaje
        msg = Message(
            form.username.data + ' le ha escrito un nuevo mensaje',
            recipients=['mmesa_@hotmail.com'])

        msg.body = form.message.data
        mail.send(msg)
        return jsonify({'success': 'Su mensaje se ha enviado correctamente'})

    return jsonify({'error': 'Algo salio mal, verifique los datos!'})


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Renderiza el login """
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

        return 'Nombre de usuario o Contraseña invalidos!'

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """ Renderiza el logout """
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    """ Renderiza el dashboard """
    cursor = connectiondb.cursor()
    sql = "SELECT * FROM Comentario ORDER BY id DESC"
    cursor.execute(sql)
    comentarios = cursor.fetchall()
    cursor.close()

    return render_template('dashboard.html',
                           name=current_user.username,
                           form=comentarios)


@app.route('/dashboard/mensajes/<id_mensaje>')
@login_required
def mensajes(id_mensaje):
    """ Muestra el mensaje seleccionado """
    cursor = connectiondb.cursor()
    sql = "SELECT * FROM Comentario WHERE id = '%s'" % id_mensaje
    cursor.execute(sql)
    mensaje = cursor.fetchall()
    cursor.close()
    return render_template('messages.html',
                           form=mensaje,
                           name=current_user.username)


@app.route('/parametros', methods=['GET', 'POST'])
@login_required
def parametros():
    """ Renderiza parametros """
    form = FormParametrosFactura()

    return render_template('parametros_factura.html',
                           form=form,
                           name=current_user.username)


@app.route('/procesa_parametros_factura', methods=['POST'])
@login_required
def procesa_parametros_factura():
    """ Procesa el formulario parametros factura """
    form = FormParametrosFactura()

    if request.method == 'POST' and form.validate_on_submit():
        cursor_insert = connectiondb.cursor()
        cursor_update = connectiondb.cursor()
        cursor_select = connectiondb.cursor()
        # verifica si existen datos en la tabla
        sql_select = """SELECT num_fac_ini FROM ParametrosFactura"""
        cursor_select.execute(sql_select)
        resultado = cursor_select.fetchone()
        cursor_select.close()

        if resultado is None:
            sql_insert = """INSERT INTO ParametrosFactura (num_fac_ini, num_fac_fin, \
                            num_resolucion, fecha_resolucion,
                            fecha_venc_resolucion) \
                            VALUES ('{}', '{}', '{}', '{}', '{}');
                            """.format(form.num_fac_ini.data,
                                       form.num_fac_fin.data,
                                       form.num_resolucion.data,
                                       form.fecha_resolucion.data,
                                       form.fecha_venc_resolucion.data)

            cursor_insert.execute(sql_insert)
            connectiondb.commit()
            cursor_insert.close()
            # connectiondb.close()
            return "Los datos se guardaron correctamente"
        else:
            sql_update = """UPDATE ParametrosFactura \
                            SET num_fac_ini = '{}', \
                                num_fac_fin = '{}', \
                                num_resolucion = '{}', \
                                fecha_resolucion = '{}',
                                fecha_venc_resolucion = '{}' \
                            WHERE num_fac_ini = '{}';
                            """.format(form.num_fac_ini.data,
                                       form.num_fac_fin.data,
                                       form.num_resolucion.data,
                                       form.fecha_resolucion.data,
                                       form.fecha_venc_resolucion.data,
                                       int(resultado['num_fac_ini']))

            cursor_update.execute(sql_update)
            connectiondb.commit()
            cursor_update.close()
            connectiondb.close()
            return "Los datos se guardaron correctamente"


@app.route('/nueva_factura', methods=['GET', 'POST'])
@login_required
def nueva_factura():
    """ Captura datos de una nueva factura """
    num_fac = str(generar_numero_factura())

    return render_template('facturar.html',
                           numero_factura=num_fac,
                           name=current_user.username)


@app.route('/guarda_factura', methods=['GET', 'POST'])
@login_required
def guarda_factura():
    content = request.json
    print type(content)
    return jsonify({'success': content['cliente']})

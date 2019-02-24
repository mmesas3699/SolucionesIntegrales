# -*- coding: utf-8 -*-
"""Se definen las vistas de la aplicacion."""

from flask_mail import Message
from werkzeug.security import check_password_hash  # generate_password_hash,
from flask_login import login_user, login_required, logout_user, current_user
from flask_weasyprint import HTML, render_pdf

# from flask import make_response
from flask import render_template, redirect, url_for, request, jsonify

from app import app, db, mail, connectiondb
from .forms import CommentForm, LoginForm, FormParametrosFactura
from .models import Comentario, User


# ............ Controladores .................

def generar_numero_factura():
    """Genera los números de factura"""
    cursor_fac = connectiondb.cursor()
    cursor_param = connectiondb.cursor()
    sql_select_fac = """SELECT num_factura
                        FROM Factura
                        ORDER BY num_factura DESC LIMIT 1;"""
    sql_select_param = """SELECT num_fac_ini, num_fac_fin, factura_actual
                          FROM ParametrosFactura;"""

    cursor_fac.execute(sql_select_fac)
    resultado_fac = cursor_fac.fetchall()
    cursor_fac.close()
    cursor_param.execute(sql_select_param)
    resultado_param = cursor_param.fetchall()
    cursor_param.close()

    print(resultado_param)
    if len(resultado_fac) == 0:
        if len(resultado_param) == 0:
            return "Falta capturar los consecutivos de las facturas"
        elif resultado_param[0]['factura_actual']:
            numero_factura = resultado_param[0]['factura_actual']
            return str(numero_factura)
        else:
            numero_factura = resultado_param[0]['num_fac_ini']
            return str(numero_factura)
    elif resultado_fac[0]['num_factura'] > resultado_param[0]['num_fac_fin']:
        return "Debe actualizar el consecutivo de las facturas"
    else:
        numero_factura = resultado_fac[0]['num_factura'] + 1
        return str(numero_factura)


def sql_guarda_factura(n_factura, fec_factura, iden_cliente,
                       subtotal, val_iva, val_total):

    cursor_factura = connectiondb.cursor()

    sql_guarda_fac = """INSERT INTO Factura(num_factura,
                                            fecha_factura,
                                            identificacion_cliente,
                                            sub_total,
                                            val_iva,
                                            val_total)
                        VAlUES ('{}','{}','{}',
                                '{}','{}','{}');""".format(n_factura,
                                                           fec_factura,
                                                           iden_cliente,
                                                           subtotal,
                                                           val_iva,
                                                           val_total)

    try:
        cursor_factura.execute(sql_guarda_fac)
        connectiondb.commit()
        return 'OK'
    except Exception as e:
        connectiondb.rollback()
        raise e
    finally:
        cursor_factura.close()


def sql_guarda_cliente(iden, nombre, direccion, ciudad, tel):
    ide = iden
    sql_clien = """SELECT identificacion_cliente
                   FROM Cliente
                   WHERE identificacion_cliente = '{}';""".format(ide)

    cursor_clien = connectiondb.cursor()
    cursor_clien.execute(sql_clien)
    res = cursor_clien.fetchall()
    cursor_clien.close()

    if len(res) == 0:
        sql_guarda_cli = """INSERT INTO Cliente(identificacion_cliente,
                                                nombre_cliente,
                                                direccion,
                                                ciudad,
                                                telefono)
                            VALUES ('{}', '{}', '{}',
                                    '{}', '{}');""".format(iden,
                                                           nombre,
                                                           direccion,
                                                           ciudad,
                                                           tel)
        try:
            cursor_cliente = connectiondb.cursor()
            cursor_cliente.execute(sql_guarda_cli)
            connectiondb.commit()
            return 'OK'
        except Exception as e:
            raise e
            connectiondb.rollback()
        finally:
            cursor_cliente.close()


def guarda_items_factura(num_fac, consecutivo, ref, valUnit, cant, porIva,
                         valIva, totItem):

    sql_guarda_items = """INSERT INTO ItemsFactura (num_factura,
                                                    consecutivo,
                                                    referencia,
                                                    val_unitario,
                                                    cantidad_item,
                                                    porcentaje_iva,
                                                    valor_iva_item,
                                                    valor_item)
                           VALUES ('{}','{}','{}',
                                   '{}','{}','{}',
                                   '{}','{}');""".format(num_fac,
                                                         consecutivo,
                                                         ref,
                                                         valUnit,
                                                         cant,
                                                         porIva,
                                                         valIva,
                                                         totItem)

    try:
        cursor_items_factura = connectiondb.cursor()
        cursor_items_factura.execute(sql_guarda_items)
        connectiondb.commit()
        return 'OK'
    except Exception as e:
        raise e
        connectiondb.rollback()
    finally:
        cursor_items_factura.close()


# ---------------- Remisiones

def sql_guarda_remision(num_rem, fec_rem, iden_cliente,
                        subtotal, val_iva, val_total, observaciones):

    cursor_remision = connectiondb.cursor()

    sql_guarda_rem = """INSERT INTO Remision(num_remision,
                                             fecha_remision,
                                             identificacion_cliente,
                                             sub_total,
                                             val_iva,
                                             val_total,
                                             observaciones)
                        VAlUES ('{}','{}','{}',
                                '{}','{}','{}','{}');""".format(num_rem,
                                                           fec_rem,
                                                           iden_cliente,
                                                           subtotal,
                                                           val_iva,
                                                           val_total,
                                                           observaciones)

    try:
        cursor_remision.execute(sql_guarda_rem)
        connectiondb.commit()
        return 'OK'
    except Exception as e:
        connectiondb.rollback()
        raise e
    finally:
        cursor_remision.close()


def guarda_items_remision(num_rem, consecutivo, ref, valUnit, cant, porIva,
                          valIva, totItem):
    sql_guarda_items = """INSERT INTO ItemsRemision(num_remision,
                                                    consecutivo,
                                                    referencia,
                                                    val_unitario,
                                                    cantidad_item,
                                                    porcentaje_iva,
                                                    valor_iva_item,
                                                    valor_item)
                           VALUES ('{}','{}','{}',
                                   '{}','{}','{}',
                                   '{}','{}');""".format(num_rem,
                                                         consecutivo,
                                                         ref,
                                                         valUnit,
                                                         cant,
                                                         porIva,
                                                         valIva,
                                                         totItem)

    try:
        cursor_items_remision = connectiondb.cursor()
        cursor_items_remision.execute(sql_guarda_items)
        connectiondb.commit()
        return 'OK'
    except Exception as e:
        raise e
        connectiondb.rollback()
    finally:
        cursor_items_remision.close()

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
    cursor = connectiondb.cursor()
    sql = "SELECT * FROM ParametrosFactura"
    cursor.execute(sql)
    parametro = cursor.fetchall()
    cursor.close()

    if parametro:
        return redirect(url_for('consulta_parametros'))
    else:
        return render_template('parametros_factura.html',
                               form=form,
                               name=current_user.username)


@app.route('/consulta_parametros')
@login_required
def consulta_parametros():
    """ Para consultar los parametros creados"""
    cursor = connectiondb.cursor()
    sql = "SELECT * FROM ParametrosFactura"
    cursor.execute(sql)
    parametro = cursor.fetchall()
    cursor.close()

    print parametro
    return render_template('consulta_parametros.html',
                           parametros=parametro,
                           name=current_user.username)


@app.route('/procesa_parametros_factura', methods=['POST'])
@login_required
def procesa_parametros_factura():
    """Guarda o actualiza los parametros de las factutas."""
    form = FormParametrosFactura()
    print(form.num_fac_ini.data, form.factura_actual.data)

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
            sql_insert = """INSERT INTO ParametrosFactura (num_fac_ini, \
                num_fac_fin, num_resolucion, fecha_resolucion, \
                fecha_venc_resolucion, factura_actual) VALUES \
                ('{}', '{}', '{}', '{}', '{}', '{}');
                """.format(form.num_fac_ini.data, form.num_fac_fin.data,
                           form.num_resolucion.data, form.fecha_resolucion.data,
                           form.fecha_venc_resolucion.data, form.factura_actual.data)
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
                                fecha_venc_resolucion = '{}', \
                                factura_actual = '{}' \
                            WHERE num_fac_ini = '{}';
                            """.format(form.num_fac_ini.data,
                                       form.num_fac_fin.data,
                                       form.num_resolucion.data,
                                       form.fecha_resolucion.data,
                                       form.fecha_venc_resolucion.data,
                                       form.factura_actual.data,
                                       int(resultado['num_fac_ini']))

            cursor_update.execute(sql_update)
            connectiondb.commit()
            cursor_update.close()
            return "Los datos se guardaron correctamente"


@app.route('/actualiza_parametros')
@login_required
def actualiza_parametros():
    """ actualiza los parametros"""
    form = FormParametrosFactura()

    return render_template('parametros_factura.html',
                           form=form,
                           name=current_user.username)


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
    data = request.json

    numero_factura = int(data['numfactura'])
    iden_cliente = int(data['identificacion'])
    cliente = data['cliente']
    direccion = data['direccion']
    ciudad = data['ciudad']
    telefono = data['telefono']
    fecha = (data['fecha'])
    subtotal = int(data['subtotal'].replace(',', ''))
    iva = int(data['iva'].replace(',', ''))
    total = int(data['total'].replace(',', ''))
    items = data['items']

    sql_guarda_factura(numero_factura, fecha, iden_cliente,
                       subtotal, iva, total)

    sql_guarda_cliente(iden_cliente, cliente, direccion,
                       ciudad, telefono)

    for item in items:
        consecutivo = items.index(item) + 1
        fact = numero_factura
        ref = item[0]
        valUnit = item[1]
        cant = item[2]
        porIva = item[3]
        valIva = item[4]
        totItem = item[5]
        guarda_items_factura(fact,
                             consecutivo,
                             ref,
                             valUnit,
                             cant,
                             porIva,
                             valIva,
                             totItem)

    return jsonify({'success': 'Factura guardada correctamente'})


@app.route('/consulta-facturas')
@login_required
def consulta_facturas():
    """ Renderiza el dashboard """
    cursor = connectiondb.cursor()
    sql = """SELECT Factura.num_factura, Cliente.nombre_cliente,
             Factura.fecha_factura, Factura.val_total
             FROM Factura
             INNER JOIN Cliente
             ON Factura.identificacion_cliente = Cliente.identificacion_cliente
             ORDER BY Factura.num_factura DESC;"""
    cursor.execute(sql)
    facturas = cursor.fetchall()
    cursor.close()

    return render_template('consulta-facturas.html',
                           name=current_user.username,
                           form=facturas)


@app.route('/dashboard/factura/<num_factura>')
@login_required
def factura(num_factura):
    """ Muestra la factura seleccionada """
    cursor_factura = connectiondb.cursor()
    sql_factura = """SELECT * FROM Factura
                     WHERE num_factura = '%s'""" % num_factura
    cursor_factura.execute(sql_factura)
    factura = cursor_factura.fetchone()
    cursor_factura.close()

    cursor_items_factura = connectiondb.cursor()
    sql_items_factura = """SELECT * FROM ItemsFactura
                           WHERE num_factura = '%s'""" % num_factura
    cursor_items_factura.execute(sql_items_factura)
    items_factura = cursor_items_factura.fetchall()
    cursor_items_factura.close()

    cursor_parametros = connectiondb.cursor()
    sql_parametros = """SELECT * FROM ParametrosFactura"""
    cursor_parametros.execute(sql_parametros)
    parametros = cursor_parametros.fetchone()
    cursor_parametros.close()

    # Formatea el numero de factura para la resolución
    cero = '0'
    param_num_fac_ini = str(parametros['num_fac_ini'])
    param_num_fac_fin = str(parametros['num_fac_fin'])
    while len(param_num_fac_ini) < len(param_num_fac_fin):
        param_num_fac_ini = cero[:] + param_num_fac_ini

    # Formatea el numero de factura
    numero_factura = str(factura['num_factura'])
    ultm_consecutivo = str(parametros['num_fac_fin'])

    while len(numero_factura) < len(ultm_consecutivo):
        numero_factura = cero[:] + numero_factura

    # Datos del cliente
    cursor_datos_cliente = connectiondb.cursor()
    sql_datos_cliente = """SELECT Factura.num_factura, Cliente.nombre_cliente,
                           Cliente.identificacion_cliente, Cliente.direccion,
                           Cliente.ciudad, Cliente.telefono
                           FROM Factura
                           INNER JOIN Cliente
                           ON Factura.identificacion_cliente = Cliente.identificacion_cliente
                           WHERE Factura.num_factura = '{}'
                           ORDER BY Factura.num_factura DESC;""".format(factura['num_factura'])
    cursor_datos_cliente.execute(sql_datos_cliente)
    datos_cliente = cursor_datos_cliente.fetchone()
    cursor_datos_cliente.close()

    return render_template('factura.html',
                           parametros=parametros,
                           param_num_fac_ini=param_num_fac_ini,
                           datos_cliente=datos_cliente,
                           factura=factura,
                           numero_factura=numero_factura,
                           items_factura=items_factura,
                           name=current_user.username)


@app.route('/dashboard/factura/pdf/<num_factura>')
@login_required
def pdf(num_factura):
    cursor_factura = connectiondb.cursor()
    sql_factura = """SELECT * FROM Factura
                     WHERE num_factura = '%s'""" % num_factura
    cursor_factura.execute(sql_factura)
    factura = cursor_factura.fetchone()
    cursor_factura.close()

    # Formato a los valores de la factura
    factura['sub_total'] = format(factura['sub_total'], ",d")
    factura['val_iva'] = format(factura['val_iva'], ",d")
    factura['val_total'] = format(factura['val_total'], ",d")

    cursor_items_factura = connectiondb.cursor()
    sql_items_factura = """SELECT cantidad_item, referencia, val_unitario,
                                  valor_item
                           FROM ItemsFactura
                           WHERE num_factura = '%s'""" % num_factura
    cursor_items_factura.execute(sql_items_factura)
    items_factura = cursor_items_factura.fetchall()
    cursor_items_factura.close()

    for item in items_factura:
        item['val_unitario'] = format(item['val_unitario'], ",d")
        item['valor_item'] = format(item['valor_item'], ",d")

    cursor_parametros = connectiondb.cursor()
    sql_parametros = """SELECT * FROM ParametrosFactura"""
    cursor_parametros.execute(sql_parametros)
    parametros = cursor_parametros.fetchone()
    cursor_parametros.close()

    # Formatea el numero de factura para la resolución
    cero = '0'
    param_num_fac_ini = str(parametros['num_fac_ini'])
    param_num_fac_fin = str(parametros['num_fac_fin'])
    while len(param_num_fac_ini) < len(param_num_fac_fin):
        param_num_fac_ini = cero[:] + param_num_fac_ini

    # Formatea el numero de factura
    numero_factura = str(factura['num_factura'])
    ultm_consecutivo = str(parametros['num_fac_fin'])

    while len(numero_factura) < len(ultm_consecutivo):
        numero_factura = cero[:] + numero_factura

    # Datos del cliente
    cursor_datos_cliente = connectiondb.cursor()
    sql_datos_cliente = """SELECT Factura.num_factura, Cliente.nombre_cliente,
                           Cliente.identificacion_cliente, Cliente.direccion,
                           Cliente.ciudad, Cliente.telefono
                           FROM Factura
                           INNER JOIN Cliente
                           ON Factura.identificacion_cliente = Cliente.identificacion_cliente
                           WHERE Factura.num_factura = '{}'
                           ORDER BY Factura.num_factura DESC;""".format(factura['num_factura'])
    cursor_datos_cliente.execute(sql_datos_cliente)
    datos_cliente = cursor_datos_cliente.fetchone()
    cursor_datos_cliente.close()

    html = render_template('factura-pdf.html',
                           parametros=parametros,
                           param_num_fac_ini=param_num_fac_ini,
                           datos_cliente=datos_cliente,
                           factura=factura,
                           numero_factura=numero_factura,
                           items_factura=items_factura,
                           name=current_user.username)

    return render_pdf(HTML(string=html))


@app.route('/remision', methods=['GET', 'POST'])
@login_required
def nueva_remision():
    """ Captura datos de una nueva remision """

    return render_template('remision.html',
                           name=current_user.username)


@app.route('/guarda_remision', methods=['GET', 'POST'])
@login_required
def guarda_remision():
    data = request.json

    sql_num_rem = """SELECT num_remision FROM Remision ORDER BY num_remision
                     DESC LIMIT 1;"""

    cursor_num_rem = connectiondb.cursor()
    cursor_num_rem.execute(sql_num_rem)
    rem = cursor_num_rem.fetchone()
    cursor_num_rem.close()

    if rem is None:
        rem = 1
    else:
        rem = rem['num_remision'] + 1

    iden_cliente = int(data['identificacion'])
    cliente = data['cliente']
    direccion = data['direccion']
    ciudad = data['ciudad']
    telefono = data['telefono']
    fecha = (data['fecha'])
    subtotal = int(data['subtotal'].replace(',', ''))
    iva = int(data['iva'].replace(',', ''))
    total = int(data['total'].replace(',', ''))
    items = data['items']
    observaciones = data['condiciones']

    sql_guarda_remision(rem, fecha, iden_cliente,
                        subtotal, iva, total, observaciones)

    sql_guarda_cliente(iden_cliente, cliente, direccion,
                       ciudad, telefono)

    for item in items:
        rem = rem
        ref = item[0]
        consecutivo = items.index(item) + 1
        valUnit = item[1]
        cant = item[2]
        porIva = item[3]
        valIva = item[4]
        totItem = item[5]
        guarda_items_remision(rem,
                              consecutivo,
                              ref,
                              valUnit,
                              cant,
                              porIva,
                              valIva,
                              totItem)

    return jsonify({'success': 'Remision guardada correctamente'})


@app.route('/remisiones')
@login_required
def remisiones():
    """ Consulta de remisiones """
    cursor = connectiondb.cursor()
    sql = """SELECT Remision.num_remision, Cliente.nombre_cliente,
             Remision.fecha_remision, Remision.val_total
             FROM Remision
             INNER JOIN Cliente
             ON Remision.identificacion_cliente = Cliente.identificacion_cliente
             ORDER BY Remision.num_remision DESC;"""
    cursor.execute(sql)
    remisiones = cursor.fetchall()
    cursor.close()

    return render_template('remisiones.html',
                           name=current_user.username,
                           form=remisiones)


@app.route('/dashboard/remisiones/pdf/<num_remision>')
@login_required
def remision(num_remision):
    """ Imprimir Remisión """

    cursor_remision = connectiondb.cursor()
    sql_remision = """SELECT * FROM Remision
                     WHERE num_remision = '%s'""" % num_remision
    cursor_remision.execute(sql_remision)
    remision = cursor_remision.fetchone()
    cursor_remision.close()

    # Formato a los valores de la remision
    remision['sub_total'] = format(remision['sub_total'], ",d")
    remision['val_iva'] = format(remision['val_iva'], ",d")
    remision['val_total'] = format(remision['val_total'], ",d")

    cursor_items_remision = connectiondb.cursor()
    sql_items_remision = """SELECT consecutivo, cantidad_item, 
                                  referencia, val_unitario,
                                  valor_item
                           FROM ItemsRemision
                           WHERE num_remision = '%s'""" % num_remision
    cursor_items_remision.execute(sql_items_remision)
    items_remision = cursor_items_remision.fetchall()
    cursor_items_remision.close()

    for item in items_remision:
        item['val_unitario'] = format(item['val_unitario'], ",d")
        item['valor_item'] = format(item['valor_item'], ",d")

    # Datos del cliente
    cursor_datos_cliente = connectiondb.cursor()
    sql_datos_cliente = """SELECT Remision.num_remision, Cliente.nombre_cliente,
                           Cliente.identificacion_cliente, Cliente.direccion,
                           Cliente.ciudad, Cliente.telefono
                           FROM Remision
                           INNER JOIN Cliente
                           ON Remision.identificacion_cliente = Cliente.identificacion_cliente
                           WHERE Remision.num_remision = '{}'
                           ORDER BY Remision.num_remision DESC;""".format(remision['num_remision'])
    cursor_datos_cliente.execute(sql_datos_cliente)
    datos_cliente = cursor_datos_cliente.fetchone()
    cursor_datos_cliente.close()

    html = render_template('remision-pdf.html',
                           remision=remision,
                           datos_cliente=datos_cliente,
                           items_remision=items_remision,
                           name=current_user.username)

    return render_pdf(HTML(string=html))

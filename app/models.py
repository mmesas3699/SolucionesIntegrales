# -*- coding: utf-8 -*-

from flask_login import UserMixin


from app import db, login_manager

"""
Para hacer las migraciones:
>>> from app import db
>>> db.create_all()
"""

class Comentario(db.Model):
    """
    Crea la tabla Comentario
    """

    __tablename__ = 'Comentario'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nombre = db.Column(db.String(60))
    email = db.Column(db.String(60))
    mensaje = db.Column(db.Text(2000))
    indicador_lectura = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime)

    def __repr__(self):
        return '<Comentario: {} {} {}>'.format(
            self.nombre, self.email, self.mensaje)


class User(UserMixin, db.Model):

    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(256), unique=False)

    # from werkzeug.security import generate_password_hash
    # from app.models import User
    # me = User(username='user', password=generate_password_hash('password'))
    # db.session.add(me)
    # db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ParametrosFactura(db.Model):

    __tablename__ = 'ParametrosFactura'

    num_fac_ini = db.Column(db.Integer,)
    num_fac_fin = db.Column(db.Integer)
    num_resolucion = db.Column(
        db.String(30), primary_key=True)
    fecha_resolucion = db.Column(db.DateTime)
    fecha_venc_resolucion = db.Column(db.DateTime)
    # Para digitar el número de factura en la cual debe iniciar la facturación.
    factura_actual = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<ParametrosFactura: {} {} {}'.format(
            self.num_fac_ini, self.num_fac_fin, self.num_resolucion)


class Factura(db.Model):

    __tablename__ = 'Factura'

    num_factura = db.Column(db.BigInteger,
                            primary_key=True,
                            autoincrement=False)
    fecha_factura = db.Column(db.DateTime)
    identificacion_cliente = db.Column(db.String(10))
    sub_total = db.Column(db.Integer)
    val_iva = db.Column(db.Integer)
    val_total = db.Column(db.Integer)


class ItemsFactura(db.Model):

    __tablename__ = 'ItemsFactura'

    num_factura = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=False)
    consecutivo = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=False)
    referencia = db.Column(db.String(3000))
    val_unitario = db.Column(db.Integer)
    cantidad_item = db.Column(db.Integer)
    porcentaje_iva = db.Column(db.Float)
    valor_iva_item = db.Column(db.Integer)
    valor_item = db.Column(db.Integer)


class Cliente(db.Model):

    __tablename__ = 'Cliente'

    identificacion_cliente = db.Column(db.String(10), primary_key=True)
    nombre_cliente = db.Column(db.String(70))
    direccion = db.Column(db.String(70))
    ciudad = db.Column(db.String(50))
    telefono = db.Column(db.String(50))


class Remision(db.Model):

    __tablename__ = 'Remision'

    num_remision = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=False)
    fecha_remision = db.Column(db.DateTime)
    identificacion_cliente = db.Column(db.BigInteger)
    sub_total = db.Column(db.Integer)
    val_iva = db.Column(db.Integer)
    val_total = db.Column(db.Integer)
    observaciones = db.Column(db.Text(3000))

class ItemsRemision(db.Model):

    __tablename__ = 'ItemsRemision'

    num_remision = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=False)
    consecutivo = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=False)
    referencia = db.Column(db.String(2000))
    val_unitario = db.Column(db.Integer)
    cantidad_item = db.Column(db.Integer)
    porcentaje_iva = db.Column(db.Float)
    valor_iva_item = db.Column(db.Integer)
    valor_item = db.Column(db.Integer)

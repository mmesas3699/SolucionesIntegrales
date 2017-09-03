# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask_login import UserMixin


from app import db, login_manager


class Comentario(db.Model):
    """
    Crea la tabla Comentario
    """

    __tablename__ = 'comentario'

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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(256), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ParametrosFactura(db.Model):

    __tablename__ = 'ParametrosFactura'

    num_fac_ini = db.Column(db.Integer, primary_key=True)
    num_fac_fin = db.Column(db.Integer)
    num_resolucion = db.Column(db.Integer)
    fecha_resolucion = db.Column(db.DateTime)

    def __repr__(self):
        return '<ParametrosFactura: {} {} {}'.format(self.num_fac_ini,
                                                     self.num_fac_fin,
                                                     self.num_resolucion)

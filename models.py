from webapp import db
from flask_login import UserMixin
import datetime

class Fornecedores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    cnpj = db.Column(db.String(30), nullable=False)
    ramo = db.Column(db.String(30), nullable=False)
    endereco = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    datetime_subscription_valid_until = db.Column(db.DateTime, default=datetime.datetime.utcnow() - datetime.timedelta(days=1))
    datetime_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Name %r>' % self.name
    
    

    

    
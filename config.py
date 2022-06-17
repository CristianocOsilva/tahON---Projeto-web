import os

SECRET_KEY = "random string"
SQLALCHEMY_TRACK_MODIFICATIONS = False
LESS_BIN = '/usr/local/bin/lessc'
ASSETS_DEBUG = False
ASSETS_AUTO_BUILD = True

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '#Computacao2354',
        servidor = 'localhost',
        database = 'fornecedor'
    )

#UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
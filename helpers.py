import os
from webapp import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioFornecedor(FlaskForm):
    nome = StringField('Nome da Empresa', [validators.DataRequired(), validators.Length(min=1, max=50)])
    cnpj = StringField('CNPJ', [validators.DataRequired(), validators.Length(min=1, max=30)])
    ramo = StringField('ramo de atividade', [validators.DataRequired(), validators.Length(min=1, max=30)])
    endereco = StringField('endereco', [validators.DataRequired(), validators.Length(min=1, max=50)])
    telefone = StringField('telefone', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=1, max=50)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH']), arquivo)












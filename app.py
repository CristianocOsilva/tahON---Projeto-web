from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fornecedores.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class fornecedores(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   nome = db.Column(db.String(100))
   produto = db.Column(db.String(100))
   email = db.Column(db.String(200)) 
   endereco = db.Column(db.String(150))

   def __init__(self, nome, produto, email, endereco):
      self.nome = nome
      self.produto = produto
      self.email = email
      self.endereco = endereco


@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/fornecedores')
def tabela():
   return render_template('fornecedores.html', fornecedores = fornecedores.query.all() )

@app.route('/cadastro', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['nome'] or not request.form['produto'] or not request.form['email']:
         flash('Preencher todos os campos', 'Erro')
      else:
         fornecedor = fornecedores(request.form['nome'], request.form['produto'], request.form['email'], request.form['endereco'])
         db.session.add(fornecedor)
         db.session.commit()
         flash('Registro adicionado com Sucesso')
         return redirect(url_for('tabela'))
   return render_template('cadastro.html')

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
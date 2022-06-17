from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from webapp import app, db
from models import *
from helpers import * 
from flask_bcrypt import check_password_hash
import services
import time
from api_mercadopago import payment
from flask_login import  login_manager
from flask_login import current_user, login_required, logout_user, login_user
from flask_assets import Bundle, Environment
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/cadastro', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['nome'] or not request.form['produto'] or not request.form['email']:
         flash('Preencher todos os campos', 'Erro')
      else:
         fornecedor = fornecedores(request.form['nome'], request.form['cnpj'], request.form['ramo'], request.form['endereco'], request.form['telefone'])
         db.session.add(fornecedor)
         db.session.commit()
         flash('Registro adicionado com Sucesso')
         return redirect(url_for('fornecedores'))
   return render_template('cadastro.html')

@app.route('/catalogo')
def catalogo():
    products = services.get_products()
    return render_template('products.html', products=products)


@app.route('/buy/<int:id_product>')
def buy_product(id_product):
    product = services.get_product_id(id_product)
    return redirect(payment(request, product=product))
    
def compile_static_assets(app):
   
    assets = Environment(app)
    Environment.auto_build = True
    Environment.debug = False
    # Stylesheets Bundles
    account_less_bundle = Bundle(
        "src/less/account.less",
        filters="less,cssmin",
        output="dist/css/account.css",
        extra={"rel": "stylesheet/less"},
    )
    dashboard_less_bundle = Bundle(
        "src/less/dashboard.less",
        filters="less,cssmin",
        output="dist/css/dashboard.css",
        extra={"rel": "stylesheet/less"},
    )
    # JavaScript Bundle
    js_bundle = Bundle("src/js/main.js", filters="jsmin", output="dist/js/main.min.js")
    # Register assets
    assets.register("account_less_bundle", account_less_bundle)
    assets.register("dashboard_less_bundle", dashboard_less_bundle)
    assets.register("js_all", js_bundle)
    # Build assets
    account_less_bundle.build()
    dashboard_less_bundle.build()
    js_bundle.build()
 

@app.route("/meusdados", methods=["GET"])
@login_required
def dashboard():
    
    return render_template(
        "cadastro.html",
        title="Login",
        template="dashboard-template",
        current_user=current_user,
        body="Logado!",
    )


@app.route("/logout")
@login_required
def logout():
   
    logout_user()
    return redirect(url_for("index"))
    
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                nome=form.nome.data, email=form.email.data
            )
            user.set_(form.senha.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for("dashboard"))
        flash("Email já cadastrado !")
    return render_template(
        "signup.jinja2",
        title="Novo Cadastro",
        form=form,
        template="signup",
        body="Novo cadastro",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(senha=form.senha.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        flash("Inválido nome ou senha")
        return redirect(url_for("login"))
    return render_template(
        "login.jinja2",
        form=form,
        title="Login",
        template="login",
        body="Acesso a pagina",
    )

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("login"))


    
@app.before_first_request
def create_tables():
    db.create_all()
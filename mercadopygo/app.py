from mercadopygo import services
from mercadopygo.api_mercadopago import payment
from flask import Flask, Blueprint, request, flash, url_for, redirect, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required, logout_user, login_user
from flask_assets import Bundle, Environment
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fornecedores.db'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['LESS_BIN'] = '/usr/local/bin/lessc'
app.config['ASSETS_DEBUG'] = False
app.config['ASSETS_AUTO_BUILD'] = True

assets = Environment(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(user_id=id).first()

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

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = "cadastro"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), primary_key=False, unique=False, nullable=False)
    website = db.Column(db.String(60), index=False, unique=False, nullable=True)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    datetime_subscription_valid_until = db.Column(db.DateTime, default=datetime.datetime.utcnow() - datetime.timedelta(days=1))
    datetime_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

class SignupForm(FlaskForm):
    """User Sign-up Form."""

    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ],
    )
    confirm = PasswordField(
        "Confirm Your Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    website = StringField("Website", validators=[Optional()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """User Log-in Form."""

    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

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

@app.route('/catalogo')
def catalogo():
    products = services.get_products()
    return render_template('products.html', products=products)


@app.route('/buy/<int:id_product>')
def buy_product(id_product):
    product = services.get_product_id(id_product)
    return redirect(payment(request, product=product))
    
def compile_static_assets(app):
    """Configure static asset bundles."""
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
    """Logged-in User Dashboard."""
    return render_template(
        "dashboard.jinja2",
        title="Flask-Login Tutorial",
        template="dashboard-template",
        current_user=current_user,
        body="You are now logged in!",
    )


@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for("login"))
    
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data, email=form.email.data, website=form.website.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for("dashboard"))
        flash("A user already exists with that email address.")
    return render_template(
        "signup.jinja2",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        flash("Invalid username/password combination")
        return redirect(url_for("login"))
    return render_template(
        "login.jinja2",
        form=form,
        title="Log in.",
        template="login-page",
        body="Log in with your User account.",
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

    



if __name__ == '__main__':
   init_db()
   app.run(debug = True, port=5000)
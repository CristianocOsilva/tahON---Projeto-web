from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_login import current_user, login_required, logout_user, login_user
from flask_assets import Bundle, Environment
from flask_login import UserMixin


app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

assets = Environment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(user_id=id).first()



import routes

if __name__ == '__main__':
   app.run(debug=True, host='localhost')
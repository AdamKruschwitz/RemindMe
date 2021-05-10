from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
app.config['SESSION_TYPE'] = 'redis'
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
# REMOVE THESE FOR DEPLOYMENT
app.config["MAIL_USERNAME"] = 'remindmesmsbot@gmail.com'
app.config['MAIL_PASSWORD'] = 'safcteqsnlyvazhh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
mail = Mail(app)

from app import routes, models, tokens, email

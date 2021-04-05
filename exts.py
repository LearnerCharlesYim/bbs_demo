from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.alidayu import AlidayuAPI
from flask_whooshee import Whooshee

db = SQLAlchemy()
mail = Mail()
alidayu = AlidayuAPI()
whooshee = Whooshee()
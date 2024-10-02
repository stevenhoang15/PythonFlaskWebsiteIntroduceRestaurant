from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin

#from werkzeug.security import check_password_hash, generate_password_hash
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100), nullable=False)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booked(db.Model):
    __tablename__ = 'booked'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    dayBooked = db.Column(db.Date, default=datetime.utcnow().date())
    timeBooked = db.Column(db.Time, default=datetime.utcnow().time())
    ofPeople = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)

class Event(db.Model):
    _tablename_ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
class Chef(db.Model):
    __tablename__ = 'chef'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(100), nullable=False)

class AdminAccount(db.Model, UserMixin):
    __tablename__ = 'adminaccount'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    about = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    linkTwitter = db.Column(db.String(100), nullable=False)
    linkFacebook = db.Column(db.String(100), nullable=False)
    linkInstragram = db.Column(db.String(100), nullable=False)
    linkLinkedin = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)

    # def set_password(self, p):
    #     self.password = generate_password_hash(p)

    # def check_password(self, p):
    #     return check_password_hash(self.password, p)


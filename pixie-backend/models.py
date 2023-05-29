from flask_sqlalchemy import SQLAlchemy
from flask bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.model):
    '''User in the system'''

    __tablename__ = 'users'




def connect_db(app):
    '''Connect to the database'''

    app.app_context().push()
    db.app = app
    db.init_app(app)



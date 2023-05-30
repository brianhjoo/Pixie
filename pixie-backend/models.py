from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    '''User in the system'''

    __tablename__ = 'users'

    def __repr__(self):
        return f'<User username={self.username}>'

    username = db.Column(
        db.Text,
        nullable=False,
        primary_key=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )



def connect_db(app):
    '''Connect to the database'''

    app.app_context().push()
    db.app = app
    db.init_app(app)

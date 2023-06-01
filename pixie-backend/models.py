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

    @classmethod
    def signup(cls, username, password, first_name, last_name, email, is_admin):
        ''' Hashes password and adds user to db. '''

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_admin=is_admin,
        )

        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        ''' Find user in db with username and password. '''

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    '''Connect to the database'''

    app.app_context().push()
    db.app = app
    db.init_app(app)

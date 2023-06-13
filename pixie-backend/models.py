from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    ''' User in the system '''

    __tablename__ = 'users'

    def __repr__(self):
        return f'<User username={self.username}>'

    username = db.Column(
        db.String(50),
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

    def serialize(self):
        ''' Serialize to dictionary. '''

        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
        }

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


class Image(db.Model):
    ''' User uploaded image '''

    __tablename__ = 'images'

    def __repr__(self):
        return f'<Image id={self.id}: img={self.img_name}.{self.img_type}>'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    img_name = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    img_type = db.Column(
        db.String(20),
        nullable=False,
    )

    public = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    username = db.Column(
        db.String(50),
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


def connect_db(app):
    ''' Connect to the database '''

    app.app_context().push()
    db.app = app
    db.init_app(app)

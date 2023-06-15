from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import UniqueConstraint
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

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    images = db.relationship('Image', backref='user')

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

    __table_args__ = (
        UniqueConstraint('img_name', 'username', name='uix_img_name_username'),
    )

    def __repr__(self):
        return f'<Image id={self.id}: img={self.img_name}.{self.img_type}>'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    img_name = db.Column(
        db.String(50),
        nullable=False,
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

    @classmethod
    def upload_image(cls, img_name, img_type, public, username):
        ''' Add user image to db. '''

        image = cls(
            img_name=img_name,
            img_type=img_type,
            public=public,
            username=username,
        )

        db.session.add(image)

        return image

    def serialize(self):
        ''' Serialize to dictionary. '''

        return {
            'id': self.id,
            'img_name': self.img_name,
            'img_type': self.img_type,
            'public': self.public,
            'username': self.username,
            'timestamp': self.timestamp,
        }


def connect_db(app):
    ''' Connect to the database '''

    app.app_context().push()
    db.app = app
    db.init_app(app)

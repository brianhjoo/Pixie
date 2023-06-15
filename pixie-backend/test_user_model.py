import os
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from flask_bcrypt import Bcrypt
from models import db, User

os.environ['DATABASE_URL'] = 'postgresql:///pixie_test'

from app import app

bcrypt = Bcrypt()

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    ''' User model test '''

    def setUp(self):
        User.query.delete()

        hashed_pwd = (
            bcrypt.generate_password_hash('password')
            .decode('UTF-8')
        )

        u1 = User(
            username='u1',
            password=hashed_pwd,
            first_name='John',
            last_name='Smith',
            email='johnsmith@gmail.com',
            is_admin=False,
        )

        u2 = User(
            username='u2',
            password=hashed_pwd,
            first_name='Sally',
            last_name='Dean',
            email='sallydean@gmail.com',
            is_admin=False
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_valid_user_signup(self):
        u3 = User.signup(
            'u3',
            'password',
            'Dan',
            'Park',
            'danpark@gmail.com',
            False,
        )

        self.assertEqual(u3.username, 'u3')
        self.assertEqual(u3.email, 'danpark@gmail.com')
        # check to see if password is not original, unhashed password
        self.assertNotEqual(u3.password, 'password')
        # Bcrpyt strings start with $2b$
        self.assertTrue(u3.password.startswith('$2b$'))

    def test_invalid_user_signup(self):
        with self.assertRaises(IntegrityError):
            User.signup(
                'u1',
                'password',
                'Jen',
                'Martin',
                'jenmartin@gmail.com',
                False,
            )
            db.session.commit()

    def test_valid_user_authentication(self):
        u2 = User.query.get('u2')

        u = User.authenticate('u2', 'password')
        self.assertEqual(u2, u)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate('bad_username', 'password'))

    def test_invalid_password(self):
        self.assertFalse(User.authenticate('u2', 'bad_password'))

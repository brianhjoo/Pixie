import os
from sqlalchemy.exc import IntegrityError
from unittest import TestCase
from flask_bcrypt import Bcrypt
from models import db, User, Image

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

class ImageModelTestCase(TestCase):
    ''' Image model test '''

    def setUp(self):
        User.query.delete()
        Image.query.delete()

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

        db.session.add(u1)
        db.session.commit()

        img1 = Image(
            img_name='test_img1',
            img_type='jpg',
            public=False,
            username='u1',
        )

        img2 = Image(
            img_name='test_img2',
            img_type='png',
            public=True,
            username='u1',
        )

        db.session.add_all([img1, img2])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_upload_valid_image(self):
        img3 = Image.upload_image(
            'test_img3',
            'jpg',
            False,
            'u1',
        )

        self.assertEqual(img3.img_name, 'test_img3')
        self.assertEqual(img3.img_type, 'jpg')
        self.assertEqual(img3.public, False)
        self.assertEqual(img3.username, 'u1')

    def test_invalid_upload_image(self):
        with self.assertRaises(IntegrityError):
            Image.upload_image(
                'test_img2',
                'jpg',
                True,
                'u1'
            )
            db.session.commit()

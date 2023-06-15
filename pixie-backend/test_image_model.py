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

    def test_valid_upload_image(self):
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

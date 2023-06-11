import os
import jwt
from unittest import TestCase
from json_web_token import create_token

SECRET_KEY = os.environ.get('SECRET_KEY')


class TokenCreationTestCase(TestCase):
    ''' create token test '''

    def test_create_token_returns_valid_jwt(self):
        # create test user
        user = {
            'username': 'test_user',
            'is_admin': False,
        }

        # create new token with user data
        token = create_token(user)
        self.assertIsInstance(token, str)

        # decode the token to verify its contents
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload['username'], user['username'])
        self.assertEqual(payload['is_admin'], user['is_admin'])

    def test_create_token_with_invalid_user(self):
        # create invalid user
        user = {
            'is_admin': True,
        }

        # create new token with invalid user data
        self.assertRaises(KeyError, create_token, user)

    def test_create_token_with_no_user(self):
        user = None

        self.assertRaises(TypeError, create_token, user)
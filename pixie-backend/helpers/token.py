import os
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']


def create_token(user):
    '''return encoded JWT {username, is_admin} from user data'''

    payload = {
        'username': user['username'],
        'is_admin': user['is_admin'],
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token

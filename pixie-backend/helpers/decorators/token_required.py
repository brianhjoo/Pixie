import os
import jwt
from flask import request, jsonify
from functools import wraps

from models import User


SECRET_KEY = os.environ.get('SECRET_KEY')


def token_required(func):
    ''' Decorator that checks if user token is valid. '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        ''' Wrapper function for func. '''

        auth_header = request.headers.get('Authorization')

        if auth_header:
            token = auth_header.split(' ')[1]
        else:
            return jsonify({'message': 'Token is missing!'}, 401)

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}, 401)
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}, 401)

        return func(current_user, *args, **kwargs)

    return wrapper

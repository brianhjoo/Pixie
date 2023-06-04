import os

from flask import Flask, request, jsonify
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv

from models import db, connect_db, User
from helpers.token import create_token
from helpers.decorators.token_required import token_required

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

connect_db(app)


#============================================================== User Auth ====#

@app.route('/signup', methods=['POST'])
def signup():
    ''' Handle user signup. '''

    user_data = request.get_json()

    user = User.signup(
        username=user_data['username'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        email=user_data['email'],
        is_admin=False,
    )

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'message': 'Something went wrong!',
            'code': 'integrity_error',
            'status_code': 500,
        })

    token = create_token({
        'username': user.username,
        'is_admin': user.is_admin,
    })

    return jsonify(token=token), 201

@app.route('/login', methods=['POST'])
def login():
    ''' Handle user authentication. '''

    user_data = request.get_json()

    user = User.authenticate(
        username=user_data['username'],
        password=user_data['password'],
    )

    if user:
        token = create_token({
            'username': user.username,
            'is_admin': user.is_admin,
        })

        return jsonify(token=token)

    return jsonify({
            'message': 'Username or password is incorrect!',
            'code': 'not_found_error',
            'status_code': 404,
        })

#============================================================ User Photos ====#


@app.route('/<username>', methods=['GET'])
@token_required
def show_user_details(current_user, username):
    ''' Gets all user data including their photos. '''

    if current_user.username != username:
        return jsonify({'message': 'Forbidden'}, 403)

    user = current_user.serialize()

    return jsonify(user=user)

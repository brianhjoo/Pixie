import os
import base64
from flask import Flask, request, jsonify
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from PIL import Image

from models import db, connect_db, User
from helpers.token import create_token
from helpers.decorators.token_required import token_required
from aws import upload_file

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

connect_db(app)


def decode_and_upload_img(data):
    ''' Decodes base-64-encoded image and uploads it to AWS s3. '''

    base64_encoded_image = data['image']
    image_name = data['image_name']
    image_type = data['image_type']
    # image = base64.b64decode(base64_encoded_image.split(',')[1])
    image = base64.b64decode(base64_encoded_image)
    image_path = f'./image_holding/{image_name}.{image_type}'

    with open(image_path, 'wb') as image_file:
        image_file.write(image)

    upload_file(image_path)

    os.remove(image_path)


#=== ROUTES ===#
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


#=========================================================== User Detail =====#


@app.route('/<username>', methods=['GET'])
@token_required
def show_user_details(current_user, username):
    ''' Gets all user data including their photos. '''

    if current_user.username != username:
        return jsonify({'message': 'Forbidden'}, 403)

    user = current_user.serialize()

    return jsonify(user=user)


#=========================================================== Image Upload ====#


@app.route('/upload', methods=['POST'])
@token_required
def upload_image(current_user):
    ''' Takes user uploaded image and uploads it to AWS s3 bucket. '''

    data = request.get_json()
    decode_and_upload_img(data)

    return jsonify({'message': 'Image uploaded successfully!'})

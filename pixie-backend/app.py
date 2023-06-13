import os
import base64
from flask import Flask, request, jsonify
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from PIL import Image

from models import db, connect_db, User, Image
from helpers.json_web_token import create_token
from helpers.decorators.token_required import token_required
from aws import upload_file, download_file, list_user_files

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

connect_db(app)


def decode_and_upload_img(data, username):
    ''' Decodes base-64-encoded image and uploads it to AWS s3. '''

    base64_encoded_image = data['image']
    image_name = data['image_name']
    image_type = data['image_type']
    image = base64.b64decode(base64_encoded_image)
    image_path = f'./image_holding/{image_name}.{image_type}'

    # Writes the image data to the image_file in binary format.
    with open(image_path, 'wb') as image_file:
        image_file.write(image)

    upload_file(image_path, username)

    os.remove(image_path)

def download_and_encode_img(img_file, username):
    ''' Downloads image from s3 and encodes it to base-64. '''

    download_file(img_file, username)

    image_path = f'./image_holding/{img_file}'

    # Reads an image file, encodes its binary content into base64 format,
    # and then decodes the base64-encoded data into a UTF-8 string.
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    os.remove(image_path)

    return encoded_string


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


#================================================== User Detail & Images =====#

@app.route('/<username>', methods=['GET'])
@token_required
def show_user_details(current_user, username):
    ''' Gets all user data, including a list of all their images. '''

    user = current_user.username

    if user != username:
        return jsonify({'message': 'Forbidden'}, 403)

    img_files = list_user_files(username)

    encoded_imgs = (
        [download_and_encode_img(img_file, username) for img_file in img_files]
    )

    user = current_user.serialize()

    return jsonify(user=user, encoded_imgs=encoded_imgs)


#=========================================================== Image Upload ====#

@app.route('/upload', methods=['POST'])
@token_required
def upload_image(current_user):
    ''' Takes user uploaded image and uploads it to AWS s3 bucket. '''

    data = request.get_json()
    upload_successful = decode_and_upload_img(data, current_user.username)

    if upload_successful:
        uploaded_img = Image.upload_image(
            img_name=data['img_name'],
            img_type=data['img_type'],
            public=data['public'],
            username=current_user.username,
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
    else:
        return jsonify({
            'message': 'Could not upload image!',
            'code': 'client_error',
        })

    img = uploaded_img.serialize()

    return jsonify(img=img)

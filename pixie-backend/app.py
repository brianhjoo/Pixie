import os

from flask import Flask, request, jsonify
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv

from models import db, connect_db, User
from helpers.token import create_token

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
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
def show_user_details(username):
    ''' Gets all user data including their photos. '''

    auth_header = request.headers.get('Authorization')

    if auth_header:
        token = auth_header.split(' ')[1]
    else:
        token = ''

    print('TOKEN @@@@@@@@@: ', token)

    return jsonify('user data')

# function authenticateJWT(req, res, next) {
#   const authHeader = req.headers?.authorization;
#   if (authHeader) {
#     const token = authHeader.replace(/^[Bb]earer /, "").trim();

#     try {
#       res.locals.user = jwt.verify(token, SECRET_KEY);
#     } catch (err) {
#       /* ignore invalid tokens (but don't store user!) */
#     }
#   }
#   return next();
# }

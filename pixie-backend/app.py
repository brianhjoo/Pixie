from flask import Flask, request, redirect, render_template, flash, jsonify
from werkzeug.exceptions import Unauthorized
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)

from models import db, connect_db

connect_db(app)

app.config['SECRET_KEY'] = 'this_is_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)
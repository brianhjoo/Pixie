import os

from flask import Flask, request, redirect, render_template, flash, jsonify
from werkzeug.exceptions import Unauthorized
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv

from models import db, connect_db, User

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
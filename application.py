import os
from flask import Flask, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import jwt
import sqlalchemy
app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
import models
models.db.init_app(app)
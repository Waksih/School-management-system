###changes to the code for deployment
#frontend
BASE_URL = "https://school-management-system-4rbb.onrender.com"
#backend
import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) #initialize SQLAlchemy
migrate = Migrate(app,db) #initialize Flask-Migrate

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import json

config_path = './config.json'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quick-poll.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    if path.exists(config_path):
        with open(config_path, 'r') as config:
            data = json.loads(config.read())
            app.config.update(data)
    else:
        print(" * No config file. Using defaults.")
except:
    print(" * Failed to load config file.")

db = SQLAlchemy(app)
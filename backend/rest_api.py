#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:46:01 2017

@author: akashmantry
"""

from flask import Flask, Blueprint
from flask_restful import Api
from backend_app.resources.user import UserLogin, UserSignup
from backend_app.config import app_config
from backend_app.database.models import db


app = Flask(__name__)
api_blue_print = Blueprint('api', __name__)

config_name = 'development'
app.config.from_object(app_config[config_name])

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(api_blue_print)
api.add_resource(UserLogin, '/v1/login')
api.add_resource(UserSignup, '/v1/signup')
app.register_blueprint(api_blue_print)

app.run(host= '0.0.0.0')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:30:41 2017

@author: akashmantry
"""

from flask_restful import Resource, reqparse
from flask import request, jsonify, make_response
import uuid
from backend_app.database.models import User
from backend_app.database.schema import UserSchema
import jwt
import datetime
from functools import wraps
from .util import token_required
from backend_app.config import Config
from marshmallow import pprint
import re


def authorize_user(func):
	@wraps(func)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not auth.username or not auth.password:
			return {'success': False, 'error_code': 1, 'message': 'Login required'}, 401
		
		return func(*args, **kwargs)
	return decorated


class Authenticate(Resource):
	method_decorators = [authorize_user]


class UserLogin(Authenticate): #Authenticate

	def post(self):
		user = User.get_user_by_username(request.authorization.username)

		if not user:
			return {'success': False, 'error_code': 2, 'message': 'Incorrect username'}, 401

		if user.check_password(request.authorization.password):
		# generate token
			try:
				payload = {
					'=user_id': user.uid,
					'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
					'iat': datetime.datetime.utcnow()
				}
				token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

				return {'token': token.decode('UTF-8')}

			except Exception as e:
				print(e)

		return {'success': False, 'error_code': 2, 'message': 'Incorrect password'}, 401


class UserSignup(Resource):

	def post(self):

		parser = reqparse.RequestParser(bundle_errors=True)
		parser.add_argument('firstname', type=str, required=True, help="First name cannot be blank!",
							 location='json')
		parser.add_argument('lastname', type=str, required=True, help="Last name cannot be blank!",
							 location='json')
		parser.add_argument('username', type=str, required=True, help="Username cannot be blank!",
							 location='json')
		parser.add_argument('email', type=str, required=True, help="Email cannot be blank!",
							 location='json')
		parser.add_argument('password', type=str, required=True, help="Password cannot be blank!",
							 location='json')
		args = parser.parse_args()

		user = User.get_user_by_username(args['username'])
		if user:
			return {'success': False, 'error_code': 8, 'message': 'Username already registered'}, 401

		user = User.get_user_by_email(args['email'])
		if user:
			return {'success': False, 'error_code': 8, 'message': 'Email already registered'}, 401

		newUser = User(firstname=args['firstname'],
												lastname=args['lastname'],
												username=args['username'],
												email=args['email'],
												password=args['password'])
		
		newUser.save()

		#TODO Generate token
		return {'success': True, 'message': 'User created'}, 204
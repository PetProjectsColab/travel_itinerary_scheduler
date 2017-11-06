#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:22:42 2017

@author: akashmantry
"""

from flask import request
from functools import wraps
from backend_app.config import Config
import jwt
from backend_app.database.models import User


def token_required(func):
	@wraps(func)
	def decorated(*args, **kwargs):

		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']

		if not token:
			return {'success': False, 'error_code': 8, 'message': 'Token eis missing'}, 401

		try:
			data = jwt.decode(token, Config.SECRET_KEY)
			current_user = User.get_user_by_public_id(data['public_user_id'])
		except jwt.ExpiredSignatureError:
			return {'success': False, 'error_code': 4, 'message': 'Token expired. Please login again'}, 401
		except jwt.InvalidTokenError:
			return {'success': False, 'error_code': 5, 'message': 'Invalid token'}, 401
		except: 
			return {'success': False, 'error_code': 6, 'message': "User doesn't exist"}, 401			

		return func(current_user, *args, **kwargs)

	return decorated
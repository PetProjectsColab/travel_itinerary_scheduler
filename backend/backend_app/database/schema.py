#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:39:21 2017

@author: akashmantry
"""

from marshmallow import Schema, fields, post_load
from backend_app.database.models import User


class UserSchema(Schema):
		
	uid = fields.Integer()
	firstname = fields.Str()
	lastname = fields.Str()
	username = fields.Str()
	email = fields.Str()
	pwdhash = fields.Str()

	@post_load
	def make_user(self, data):
		return User(**data)
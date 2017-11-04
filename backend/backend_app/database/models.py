#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:35:20 2017

@author: akashmantry
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

# initialize sql-alchemy
db = SQLAlchemy()


class User(db.Model):
	"""This class represents the users table."""

	__tablename__ = 'User'

	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100), nullable=False)
	lastname = db.Column(db.String(100), nullable=False)
	username = db.Column(db.String(100), unique = True, nullable=False)
	email = db.Column(db.String(100), unique = True, nullable=False)
	pwdhash = db.Column(db.String, nullable=False)


	def __init__(self, firstname, lastname, username, email, password):
		self.firstname = firstname
		self.lastname = lastname
		self.username = username
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.uid)

	def save(self):
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all_users():
		return User.query.all()

	@staticmethod
	def get_user_by_firstname(firstname):
		return User.query.filter_by(firstname=firstname).all()

	@staticmethod
	def get_user_by_username(username):
		return User.query.filter_by(username=username).first()

	@staticmethod
	def get_user_by_email(email):
		return User.query.filter_by(email=email).first()

	@staticmethod
	def get_user_by_uid(uid):
		return User.query().filter_by(uid=uid).first()

	@staticmethod
	def get_user(filters=None):
		conditions = list()
		for attr, value in filters.items():
			conditions.append(getattr(User, attr).like("%%%s%%" % value))
		query = User.query.filter(or_(*conditions))

		return query.all()

	def delete(self, public_user_id):

		db.session.delete(self)
		db.session.commit()




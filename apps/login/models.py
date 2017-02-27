from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		print "Processing registration via UserManager"
		error = False
		msgs = []
		user = False
		alias = data.get('alias')
		name = data.get('name')
		email = data.get('email')
		password = data.get('password')
		password2 = data.get('confirm_password')
		dob = data.get('date_hired')

		if self.filter(email=email).exists():
			msgs.append("Email already exists. Please login or choose a different email.")
			error = True

		if len(email) < 5 or not EMAIL_REGEX.match(email):
			msgs.append("Invalid Email Address")
			error = True

		if not alias.isalnum() or len(alias) < 3:
			error = True
			msgs.append("Invalid Alias")

		if not len(name) >= 3:
			error = True
			msgs.append("Invalid Name")

		if len(password) <= 8:
			error = True
			msgs.append("Password must be greater than 8 characters")
		elif password != password2:
			error = True
			msgs.append("Passwords do not match")

		# 1986-05-15
		print "Date Hired:", dob
		if not dob:
			error = True
			msgs.append( 'Please provide your Hire Date')

		if not error:
			hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user = self.create(alias=alias, name=name, email=email, password=hashed, date_hired=dob)

		return {"error": error, "messages": msgs, "user": user}

	def login(self, data):
		email = data['email']
		password = data['password']
		error = True
		user = False
		msgs = []
		users = self.filter(email=email)
		if len(users) > 0:
			print users[0].email, users[0].alias, users[0].id
			# hashed = bcrypt.hashpw( password, bcrypt.gensalt( ) )
			# Check that a unhashed password matches one that has previously been
			# hashed
			if bcrypt.hashpw(password.encode(), users[0].password.encode()) == users[0].password:
				user = users[0]
				error = False

		if error:
			msgs.append("Invalid Email or Password")

		return { "error": error, "messages": msgs, "user": user }


# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=45)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	date_hired = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

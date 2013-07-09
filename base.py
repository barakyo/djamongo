"""
MongoDB backend for Djagno

Requires pymongo and MongoEngine
"""
import logging
import sys

try:
	from mongoengine import *
except ImportError as e:
	from django.core.exceptions import ImproperlyConfigured
	raise ImproperlyConfigured("Error loading MongoEngine: %s" % e)

from django.db import utils
from django.db.backends import *
from django.db.backends.signals import connection_created

class DatabaseWrapper(BaseDatabaseWrapper):
	vendor = 'djamongo'
	def __init__(self, *args, **kwargs):
		super(DatabaseWrapper, self).__init__(*args, **kwargs)

class DatabaseOperations(BaseDatabaseOperations):
	def max_name_length(self):
		return 64
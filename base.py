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
from djamongo.introspection import *

class DatabaseWrapper(BaseDatabaseWrapper):
	vendor = 'djamongo'
	def __init__(self, *args, **kwargs):
		super(DatabaseWrapper, self).__init__(*args, **kwargs)
		self.ops = DatabaseOperations(self)
		# @TODO Implement some sort of validation service?
		self.validation = BaseDatabaseValidation(self)
		self.introspection = DatabaseIntrospection(self)

	def _valid_connection(self):
		return self.connection is not None

	def _default_settings_dict(self):
		return {
			'HOST': '127.0.0.1',
			'PORT': 27017
		}

	def _cursor(self):
		cursor = None
		# Initiliaze the cursor
		if not self._valid_connection():
			# Get MongoDB defaults
			# defaults = _default_settings_dict()
			defaults = {
				'HOST': '127.0.0.1',
				'PORT': 27017
			}
			# Create a new dict based off of the settings
			connection_map = dict(self.settings_dict)
			# Update any missing fields
			connection_map.update(defaults)
			self.connection = connect(connection_map['NAME'], host=connection_map['HOST'],
				port=connection_map['PORT'], username=connection_map['USER'],
				password=connection_map['PASSWORD'])
			connection_created.send(sender=self.__class__, connection=self)
			cursor = self.connection
		return cursor


class DatabaseOperations(BaseDatabaseOperations):

	def max_name_length(self):
		return 64
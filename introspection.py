from mongoengine.fields import *

from django.db.backends import BaseDatabaseIntrospection

class DatabaseIntrospection(BaseDatabaseIntrospection):
	# Match MongoEngine fields to Django Fields 
    data_types_reverse = {
		StringField: 'TextField',
		URLField: 'TextField',
		EmailField: 'EmailField',
		IntField: 'IntegerField',
		LongField: 'IntegerField',
		FloatField: 'FloatField',
		DecimalField: 'DecimalField',
		BooleanField: 'BooleanField',
		DateTimeField: 'DateTimeField',
		FileField: 'FileField',
		ImageField: 'ImageField'
    }

    # Return a list of table names
    def get_table_list(self, cursor):
    	return cursor['thesis'].collection_names()
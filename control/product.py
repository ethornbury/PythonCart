import logging
import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from xml.dom.minidom import parse
import xml.dom.minidom

PRODUCTSTORE_NAME = 'default_productstore'

"""Configure JINJA"""
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates/')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)

	class Product(ndb.Model):
	#Represents a product
	id = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	manufacturerId = ndb.StringProperty(indexed=False)
	price = ndb.FloatProperty(indexed=False)
	stockTotal = ndb.IntegerProperty(indexed=False)
	
class ProductServiceHandler(webapp2.RequestHandler):
	# product service handler

	def get(self):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		products_query = Product.query(Product.id==product_id)
		products = products_query.fetch(1)
			
		# return a 404 error
		if len(products) < 1:
			self.error(404)
		else:	
			#Create a dictionary to store the data
			r={};
			r['id'] = products[0].id;
			r['name'] = products[0].name;
			r['manufacturerId'] = products[0].manufacturerId;
			r['price'] = products[0].price;			
			r['stockTotal'] = products[0].stockTotal;

			self.response.headers['Content-Type'] = 'text/x-json'
			self.response.write(json.dumps(r, separators=(',',':')))

	def post(self):
		#Process a HTTP POST Request for the service
		
		#Parse the json 		
		productjson = json.loads(self.request.body)

		# Check
		current_product = products.get_current_product()

		if (not current_product) or not (current_product.product_id() == productjson["id"]) :
			self.error(500)	
		else:

			products_query = Product.query(Product.id==productjson["id"])
			query_results = products_query.fetch()

			if len(query_results) > 0:
				self.error(409) #conflict
			else:
				#Create object to add to the app engine store
				product = Product(parent=data_store_key(PRODUCTSTORE_NAME))
				product.id = productjson["id"];
				product.name = productjson["name"];
				product.manufacturerId = productjson["manufacturerId"];
				product.price = productjson["price"];
				product.stockTotal = productjson["stockTotal"];

				#Store 
				product.put();
				
				#return message
				data = {}
				data['message'] = 'Updated (POST):'+productjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	
	def put(self):
		#Process a HTTP PUT Request service 
		
		#Parse the json	
		productjson = json.loads(self.request.body)

		# Check
		current_product = products.get_current_product()

		if (not current_product) or not (current_product.product_id() == productjson["id"]) :
			self.error(500)	
		else:

			products_query = Product.query(Product.id==productjson["id"])
			query_results = products_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Update 
				Product = Product(parent=data_store_key(PRODUCTSTORE_NAME))
				product.id = productjson["id"];
				product.name = productjson["name"];
				product.manufacturerId = productjson["manufacturerId"];
				product.price = productjson["price"];
				product.stockTotal = productjson["stockTotal"];

				#Store the info
				product.put();
				
				#return a message 
				data = {}
				data['message'] = 'Updated product (PUT):'+productjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self):
		#Process a HTTP PUT Request for the service
		
		#Parse the json 	
		productjson = json.loads(self.request.body)

		# Checks 
		current_product = products.get_current_product()

		if (not current_product) or not (current_product.product_id() == productjson["id"]) :
			self.error(500)	
		else:

			products_query = Product.query(Product.id==productjson["id"])
			query_results = products_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Delete object to add to the app engine store
				product = Product(parent=data_store_key(PRODUCTSTORE_NAME))
				product.id = productjson["id"];
				product.name = productjson["name"];
				product.manufacturerId = productjson["manufacturerId"];
				product.price = productjson["price"];
				product.stockTotal = productjson["stockTotal"];
				
				#use info
				product.delete();
				
				#return a message 
				data = {}
				data['message'] = 'Deleted product (PUT):'+productjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)
				
				
=======
import logging
import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from xml.dom.minidom import parse
import xml.dom.minidom

PRODUCTSTORE_NAME = 'default_productstore'

"""Configure JINJA"""
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates/')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)

	class Product(ndb.Model):
	"""Represents a product"""
	id = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	manufacturerId = ndb.StringProperty(indexed=False)
	price = ndb.FloatProperty(indexed=False)
	stockTotal = ndb.IntegerProperty(indexed=False)
	
class ProductServiceHandler(webapp2.RequestHandler):
	# user service handler

	def get(self,user_id):
		#Process a HTTP Get Request for the user service by returnng a user 
		
		#Read the user data from the data store
		users_query = User.query(User.id==user_id)
		users = users_query.fetch(1)
			
		#if there was no information for the user then we should return a 404 error
		if len(users) < 1:
			self.error(404)
		else:	
			#Create a dictionary to store the user attributes 
			r={};
			r['id'] = users[0].id;
			r['firstname'] = users[0].firstname;
			r['lastname'] = users[0].lastname;

			self.response.headers['Content-Type'] = 'text/x-json'
			self.response.write(json.dumps(r, separators=(',',':')))

	def post(self):
		"""Process a HTTP POST Request for the users service by adding a users information"""
		
		#Parse the json we received		
		userjson = json.loads(self.request.body)

		# Checks if the user is logged in
		current_user = users.get_current_user()

		if (not current_user) or not (current_user.user_id() == userjson["id"]) :
			#The request could not be completed because the uese is not logged in
			#or the user who is logged in is not the user specified by the update request
			self.error(500)	
		else:

			users_query = User.query(User.id==userjson["id"])
			query_results = users_query.fetch()

			if len(query_results) > 0:
				self.error(409) #conflict
			else:
				#Create user object to add to the app engine store
				user = User(parent=data_store_key(USERSTORE_NAME))
				user.id = userjson["id"];
				user.firstname = userjson["firstName"];
				user.lastname = userjson["lastName"];

				#Store the user info
				user.put();
				
				#return a message to the client
				data = {}
				data['message'] = 'Updated User (POST):'+userjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	
	def put(self):
		"""Process a HTTP PUT Request for the users service by updating a users information"""
		
		#Parse the json we received		
		userjson = json.loads(self.request.body)

		# Checks if the user is logged in
		current_user = users.get_current_user()

		if (not current_user) or not (current_user.user_id() == userjson["id"]) :
			#The request could not be completed because the uese is not logged in
			#or the user who is logged in is not the user specified by the update request
			self.error(500)	
		else:

			users_query = User.query(User.id==userjson["id"])
			query_results = users_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Update the user object
				user = query_results[0];
				user.firstname = userjson["firstName"];
				user.lastname = userjson["lastName"];

				#Store the user info
				user.put();
				
				#return a message to the client
				data = {}
				data['message'] = 'Updated User (PUT):'+userjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self):
		"""Process a HTTP PUT Request for the users service by updating a users information"""
		
		#Parse the json we received		
		userjson = json.loads(self.request.body)

		# Checks if the user is logged in
		current_user = users.get_current_user()

		if (not current_user) or not (current_user.user_id() == userjson["id"]) :
			#The request could not be completed because the uese is not logged in
			#or the user who is logged in is not the user specified by the update request
			self.error(500)	
		else:

			users_query = User.query(User.id==userjson["id"])
			query_results = users_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Update the user object
				user = query_results[0];
				user.firstname = userjson["firstName"];
				user.lastname = userjson["lastName"];

				#Store the user info
				user.delete();
				
				#return a message to the client
				data = {}
				data['message'] = 'Deleted User (PUT):'+userjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)
				
>>>>>>> 0121ad78b56084de7808c7989d65bf6daf127551

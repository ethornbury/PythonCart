import logging
import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from xml.dom.minidom import parse
import xml.dom.minidom


ORDERSTORE_NAME = 'default_orderstore'

"""Configure JINJA"""
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates/')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)

class Order(ndb.Model):
	#Represents a supplier
	id = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty()
	phonenumber = ndb.IntegerProperty(indexed=False)
	url = ndb.StringProperty(indexed=False)

class OrderServiceHandler(webapp2.RequestHandler):
	# service handler

	def get(self):
		"""Process a HTTP Get Request for the order service by returnng all orders"""
		logging.info("order GET called")

		#Read the order data from the data store
		orders_query = Order.query()
		orders = orders_query.fetch()
		
		result = [];

		for b in orders:
			#store each order in a dictionary
			order = {}
			order['id'] = b.id
			order['publisher'] = b.publisher
			order['author'] = b.author			
			order['title'] = b.title
			order['price'] = str(b.price)

			#add the dictionary to the list
			result.append(order);
			
		#Create a new dictionary for the results
		r={};

		#Give the results dictionary a key called orders whos value is the list of orders returned
		r['orders'] = result;
	
		self.response.headers['Content-Type'] = 'text/x-json'
		self.response.write(json.dumps(r, separators=(',',':')))

	def delete(self,order_id):
		"""Process a HTTP DELETE Request for orders by deleting a order with the specified id"""
		logging.info("Order delete called:"+order_id)


		#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#check if we already have an entry for that order
			orders_query = Order.query(Order.id==order_id)
			query_results = orders_query.fetch()

			if len(query_results) == 0:
				#Resource not found
				self.error(404)
			else:
				#Get the key of the object and deltet it from the key-value data store
				order = query_results[0]
				key = order.key
				key.delete()
				#return a message to the client
				data = {}
				data['message'] = 'Deleted Order:'+order_id
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

		
	def put(self):
		"""Process a HTTP PUT Request for the orders service by adding or updating a orders information"""

		#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:
		
			#Parse the json we received		
			orderjson = json.loads(self.request.body)

			#Check if the publisher for the order information exists
			publisher_query = Publisher.query(Publisher.id == orderjson["publisher"])
			publisher_query_results = publisher_query.fetch()
		
			if len(publisher_query_results)==0:
				#There is no publisher in our database with the specified id
				self.error(404); #not found
			else:		

				#check if we already have an entry for that order
				orders_query = Order.query(Order.id==orderjson["id"])
				query_results = orders_query.fetch()

				if len(query_results) == 0:
					#We must be adding a new order as the query returned zero results
					#Create a new instance of Order
					order = Order(parent=data_store_key(BOOKSTORE_NAME))
					order.id = orderjson["id"];
					order.title = orderjson["title"];
					order.author = orderjson["author"];
					order.publisher = orderjson["publisher"];
					order.price = float(orderjson["price"]);
			
					#Store the user info
					order.put();

					#return a message to the client
					data = {}
					data['message'] = 'Added Order (PUT):'+orderjson["id"]
					json_response = json.dumps(data)
					self.response.headers['Content-Type'] = 'text/x-json'
					self.response.write(json_response)

				else:
					#Update the order object
					order = query_results[0];
					order.title = orderjson["title"];
					order.author = orderjson["author"];
					order.publisher = orderjson["publisher"];
					order.price = float(orderjson["price"]);

					#Store the user info
					order.put();
			
					#return a message to the client
					data = {}
					data['message'] = 'Updated Order (PUT):'+orderjson["id"]
					json_response = json.dumps(data)
					self.response.headers['Content-Type'] = 'text/x-json'
					self.response.write(json_response)



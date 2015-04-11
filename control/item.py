import logging
import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from xml.dom.minidom import parse
import xml.dom.minidom

import product

ITEMSTORE_NAME = 'default_itemstore'

"""Configure JINJA"""
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates/')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)

class Item(ndb.Model):
	#Represents an item
	id = ndb.StringProperty(indexed=True)
	productId = ndb.StructuredProperty(ProductModel)
	quantity = ndb.IntegerProperty(indexed=False)
	price = ndb.FloatProperty(indexed=False)

class ItemServiceHandler(webapp2.RequestHandler):
	# item service handler

	def get(self):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		items_query = Item.query(Item.id==item_id)
		items = items_query.fetch(1)
			
		# return a 404 error
		if len(items) < 1:
			self.error(404)
		else:	
			#Create a dictionary to store the data
			r={};
			r['id'] = items[0].id;
			r['productId'] = items[0].productId;
			r['quantity'] = items[0].quantity;
			r['price'] = items[0].price;			

			self.response.headers['Content-Type'] = 'text/x-json'
			self.response.write(json.dumps(r, separators=(',',':')))

	def post(self):
		#Process a HTTP POST Request for the service
		
		#Parse the json 		
		itemjson = json.loads(self.request.body)

		# Check
		current_item = items.get_current_item()

		if (not current_item) or not (current_item.item_id() == itemjson["id"]) :
			self.error(500)	
		else:

			items_query = Item.query(Item.id==itemjson["id"])
			query_results = items_query.fetch()

			if len(query_results) > 0:
				self.error(409) #conflict
			else:
				#Create object to add to the app engine store
				item = Item(parent=data_store_key(ITEMSTORE_NAME))
				item.id = itemjson["id"];
				item.productId = itemjson["productId"];
				item.quantity = itemjson["quantity"];
				item.price = itemjson["price"];

				#Store 
				item.put();
				
				#return message
				data = {}
				data['message'] = 'Updated (POST):'+itemjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	
	def put(self):
		#Process a HTTP PUT Request service 
		
		#Parse the json	
		itemjson = json.loads(self.request.body)

		# Check
		current_item = items.get_current_item()

		if (not current_item) or not (current_item.item_id() == itemjson["id"]) :
			self.error(500)	
		else:

			items_query = Item.query(Item.id==itemjson["id"])
			query_results = items_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Update 
				item = Item(parent=data_store_key(ITEMSTORE_NAME))
				item.id = itemjson["id"];
				item.productId = itemjson["productId"];
				item.quantity = itemjson["quantity"];
				item.price = itemjson["price"];

				#Store the info
				item.put();
				
				#return a message 
				data = {}
				data['message'] = 'Updated item (PUT):'+itemjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self):
		#Process a HTTP PUT Request for the service
		
		#Parse the json 	
		itemjson = json.loads(self.request.body)

		# Checks 
		current_item = items.get_current_item()

		if (not current_item) or not (current_item.item_id() == itemjson["id"]) :
			self.error(500)	
		else:

			items_query = Item.query(Item.id==itemjson["id"])
			query_results = items_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Delete object to add to the app engine store
				item = Item(parent=data_store_key(ITEMSTORE_NAME))
				item.id = itemjson["id"];
				item.productId = itemjson["productId"];
				item.quantity = itemjson["quantity"];
				item.price = itemjson["price"];
				
				#use info
				item.delete();
				
				#return a message 
				data = {}
				data['message'] = 'Deleted item (PUT):'+itemjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

import logging
import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from xml.dom.minidom import parse
import xml.dom.minidom

import item
import user

CARTSTORE_NAME = 'default_cartstore'

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)

class Cart(ndb.Model):
	#represents a cart
	id = ndb.StringProperty(indexed=True)
	itemId = ndb.StructuredProperty(ItemModel)
	userId = ndb.StructuredProperty(UserModel)
	totalPrice = ndb.FloatProperty(indexed=False)

class CartServiceHandler(webapp2.RequestHandler):
	# service handler

	def get(self,cart_id):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		carts_query = Cart.query(Cart.id==cart_id)
		carts = carts_query.fetch(1)
			
		# return a 404 error
		if len(carts) < 1:
			self.error(404)
		else:	
			#Create a dictionary to store the data
			r={};
			r['id'] = carts[0].id;
			r['itemId'] = carts[0].itemId;
			r['userId'] = carts[0].userId;
			r['totalPrice'] = carts[0].totalPrice;			

			self.response.headers['Content-Type'] = 'text/x-json'
			self.response.write(json.dumps(r, separators=(',',':')))

	def post(self):
		#Process a HTTP POST Request for the service
		
		#Parse the json 		
		cartjson = json.loads(self.request.body)

		# Check
		current_cart = carts.get_current_cart()

		if (not current_cart) or not (current_cart.cart_id() == cartjson["id"]) :
			self.error(500)	
		else:

			carts_query = Cart.query(Cart.id==cartjson["id"])
			query_results = carts_query.fetch()

			if len(query_results) > 0:
				self.error(409) #conflict
			else:
				#Create object to add to the app engine store
				cart = Cart(parent=data_store_key(CARTSTORE_NAME_NAME))
				cart.id = cartjson["id"];
				cart.itemId = cartjson["itemId"];
				cart.userId = cartjson["userId"];
				cart.totalPrice = cartjson["totalPrice"];

				#Store 
				cart.put();
				
				#return message
				data = {}
				data['message'] = 'Updated (POST):'+cartjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	
	def put(self):
		#Process a HTTP PUT Request service 
		
		#Parse the json	
		cartjson = json.loads(self.request.body)

		# Check
		current_cart = carts.get_current_cart()

		if (not current_cart) or not (current_cart.cart_id() == cartjson["id"]) :
			self.error(500)	
		else:

			carts_query = Cart.query(Cart.id==cartjson["id"])
			query_results = carts_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Update 
				cart = Cart(parent=data_store_key(CARTSTORE_NAME_NAME))
				cart.id = cartjson["id"];
				cart.itemId = cartjson["itemId"];
				cart.userId = cartjson["userId"];
				cart.totalPrice = cartjson["totalPrice"];

				#Store the info
				cart.put();
				
				#return a message 
				data = {}
				data['message'] = 'Updated cart (PUT):'+cartjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self):
		#Process a HTTP PUT Request for the service
		
		#Parse the json 	
		cartjson = json.loads(self.request.body)

		# Checks 
		current_cart = carts.get_current_cart()

		if (not current_cart) or not (current_cart.cart_id() == cartjson["id"]) :
			self.error(500)	
		else:

			carts_query = Cart.query(Cart.id==cartjson["id"])
			query_results = carts_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Delete object to add to the app engine store
				cart = Cart(parent=data_store_key(CARTSTORE_NAME_NAME))
				cart.id = cartjson["id"];
				cart.itemId = cartjson["itemId"];
				cart.userId = cartjson["userId"];
				cart.totalPrice = cartjson["totalPrice"];
				
				#use info
				cart.delete();
				
				#return a message 
				data = {}
				data['message'] = 'Deleted cart (PUT):'+cartjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)


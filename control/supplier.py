import logging
import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from xml.dom.minidom import parse
import xml.dom.minidom


SUPPLIERSTORE_NAME = 'default_supplierstore'

"""Configure JINJA"""
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates/')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)

class Supplier(ndb.Model):
	#Represents a supplier
	id = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty()
	phonenumber = ndb.IntegerProperty(indexed=False)
	url = ndb.StringProperty(indexed=False)

class SupplierServiceHandler(webapp2.RequestHandler):
	# supplier service handler

	def get(self):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		suppliers_query = Supplier.query(Supplier.id==supplier_id)
		suppliers = suppliers_query.fetch(1)
			
		# return a 404 error
		if len(suppliers) < 1:
			self.error(404)
		else:	
			#Create a dictionary to store the data
			r={};
			r['id'] = suppliers[0].id;
			r['name'] = suppliers[0].name;
			r['email'] = suppliers[0].email;
			r['phonenumber'] = suppliers[0].phonenumber;			
			r['url'] = suppliers[0].url;

			self.response.headers['Content-Type'] = 'text/x-json'
			self.response.write(json.dumps(r, separators=(',',':')))

	def post(self):
		#Process a HTTP POST Request for the service
		
		#Parse the json 		
		supplierjson = json.loads(self.request.body)

		# Check
		current_supplier = suppliers.get_current_supplier()

		if (not current_supplier) or not (current_supplier.supplier_id() == supplierjson["id"]) :
			self.error(500)	
		else:

			suppliers_query = Supplier.query(Supplier.id==supplierjson["id"])
			query_results = suppliers_query.fetch()

			if len(query_results) > 0:
				self.error(409) #conflict
			else:
				#Create object to add to the app engine store
				supplier = Supplier(parent=data_store_key(SUPPLIERSTORE_NAME))
				supplier.id = supplierjson["id"];
				supplier.firstname = supplierjson["firstName"];
				supplier.lastname = supplierjson["lastName"];
				supplier.phonenumber = supplierjson["phonenumber"];
				supplier.url = supplierjson["url"];

				#Store 
				supplier.put();
				
				#return message
				data = {}
				data['message'] = 'Updated (POST):'+supplierjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	
	def put(self):
		#Process a HTTP PUT Request service 
		
		#Parse the json	
		supplierjson = json.loads(self.request.body)

		# Check
		current_supplier = suppliers.get_current_supplier()

		if (not current_supplier) or not (current_supplier.supplier_id() == supplierjson["id"]) :
			self.error(500)	
		else:

			suppliers_query = Supplier.query(Supplier.id==supplierjson["id"])
			query_results = suppliers_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Update 
				supplier = Supplier(parent=data_store_key(SUPPLIERSTORE_NAME))
				supplier.id = supplierjson["id"];
				supplier.firstname = supplierjson["firstName"];
				supplier.lastname = supplierjson["lastName"];
				supplier.phonenumber = supplierjson["phonenumber"];
				supplier.url = supplierjson["url"];

				#Store the info
				supplier.put();
				
				#return a message 
				data = {}
				data['message'] = 'Updated Supplier (PUT):'+supplierjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self):
		#Process a HTTP PUT Request for the service
		
		#Parse the json 	
		supplierjson = json.loads(self.request.body)

		# Checks 
		current_supplier = suppliers.get_current_supplier()

		if (not current_supplier) or not (current_supplier.supplier_id() == supplierjson["id"]) :
			self.error(500)	
		else:

			suppliers_query = Supplier.query(Supplier.id==supplierjson["id"])
			query_results = suppliers_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Delete object to add to the app engine store
				supplier = Supplier(parent=data_store_key(SUPPLIERSTORE_NAME))
				supplier.id = supplierjson["id"];
				supplier.firstname = supplierjson["firstName"];
				supplier.lastname = supplierjson["lastName"];
				supplier.phonenumber = supplierjson["phonenumber"];
				supplier.url = supplierjson["url"];
				
				#use info
				supplier.delete();
				
				#return a message 
				data = {}
				data['message'] = 'Deleted Supplier (PUT):'+supplierjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

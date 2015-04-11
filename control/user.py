import logging
import webapp2
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from xml.dom.minidom import parse
import xml.dom.minidom

USERSTORE_NAME = 'default_userstore'

"""Configure JINJA"""
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates/')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)


class User(ndb.Model):
    #represents a User entry
    id = ndb.StringProperty(indexed=True)
    firstname = ndb.StringProperty(indexed=False)
    lastname = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty()
	address = ndb.TextProperty(indexed=False)


class UserServiceHandler(webapp2.RequestHandler):
	# user service handler

	def get(self,user_id):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		users_query = User.query(User.id==user_id)
		users = users_query.fetch(1)
			
		# return a 404 error
		if len(users) < 1:
			self.error(404)
		else:	
			#Create a dictionary to store the data
			r={};
			r['id'] = users[0].id;
			r['firstname'] = users[0].firstname;
			r['lastname'] = users[0].lastname;
			r['email'] = users[0].email;
			r['address'] = users[0].address;

			self.response.headers['Content-Type'] = 'text/x-json'
			self.response.write(json.dumps(r, separators=(',',':')))

	def post(self):
		#Process a HTTP POST Request for the service
		
		#Parse the json 		
		userjson = json.loads(self.request.body)

		# Check
		current_user = users.get_current_user()

		if (not current_user) or not (current_user.user_id() == userjson["id"]) :
			self.error(500)	
		else:

			users_query = User.query(User.id==userjson["id"])
			query_results = users_query.fetch()

			if len(query_results) > 0:
				self.error(409) #conflict
			else:
				#Create object to add to the app engine store
				user = User(parent=data_store_key(USERSTORE_NAME))
				user.id = userjson["id"];
				user.firstname = userjson["firstName"];
				user.lastname = userjson["lastName"];
				user.email = userjson["email"];
				user.address = userjson["address"];

				#Store 
				user.put();
				
				#return message
				data = {}
				data['message'] = 'Updated (POST):'+userjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	
	def put(self):
		#Process a HTTP PUT Request service 
		
		#Parse the json	
		userjson = json.loads(self.request.body)

		# Check
		current_user = users.get_current_user()

		if (not current_user) or not (current_user.user_id() == userjson["id"]) :
			self.error(500)	
		else:

			users_query = User.query(User.id==userjson["id"])
			query_results = users_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				#Update 
				user = query_results[0];
				user.firstname = userjson["firstName"];
				user.lastname = userjson["lastName"];
				user.email = userjson["email"];
				user.address = userjson["address"];

				#Store the info
				user.put();
				
				#return a message 
				data = {}
				data['message'] = 'Updated User (PUT):'+userjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self):
		#Process a HTTP PUT Request for the service
		
		#Parse the json 	
		userjson = json.loads(self.request.body)

		# Checks 
		current_user = users.get_current_user()

		if (not current_user) or not (current_user.user_id() == userjson["id"]) :
			self.error(500)	
		else:

			users_query = User.query(User.id==userjson["id"])
			query_results = users_query.fetch()

			if len(query_results) == 0:
				self.error(404); #not found
			else:
				user = query_results[0];
				user.firstname = userjson["firstName"];
				user.lastname = userjson["lastName"];
				user.email = userjson["email"];
				user.address = userjson["address"];
				
				#use info
				user.delete();
				
				#return a message 
				data = {}
				data['message'] = 'Deleted User (PUT):'+userjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

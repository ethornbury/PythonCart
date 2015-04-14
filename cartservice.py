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
SUPPLIERSTORE_NAME = 'default_supplierstore'
PRODUCTSTORE_NAME = 'default_productstore'
CARTSTORE_NAME = 'default_cartstore'
ITEMSTORE_NAME = 'default_itemstore'
ORDERSTORE_NAME = 'default_orderstore'

#jinja 
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'staticpage/')),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

def data_store_key( datastore_name):
    """Constructs a datastore key for a datastore entity."""

	#Note that all my data stores are going to be under the parent EmerDatastore
    return ndb.Key('EmerDatastore', datastore_name)


class User(ndb.Model):
#represents a User entry.
	id = ndb.StringProperty(indexed=True)
	firstname = ndb.StringProperty(indexed=False)
	lastname = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty(indexed=False)
	address = ndb.TextProperty(indexed=False)
	
class Product(ndb.Model):
	#Represents a product
	id = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	supplier = ndb.StucturedProperty(Supplier)
	price = ndb.FloatProperty(indexed=False)
	stockTotal = ndb.IntegerProperty(indexed=False)
	
class Supplier(ndb.Model):
	#Represents a supplier
	id = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty(indexed=False)
	phonenumber = ndb.IntegerProperty(indexed=False)
	url = ndb.StringProperty(indexed=False)
	
class Item(ndb.Model):
	#Represents an item
	id = ndb.StringProperty(indexed=True)
	product = ndb.StructuredProperty(Product)
	quantity = ndb.IntegerProperty(indexed=False)
	
class Cart(ndb.Model):
	#represents a cart
	id = ndb.StringProperty(indexed=True)
	item = ndb.StructuredProperty(Item)
	user = ndb.StructuredProperty(User)
	totalPrice = ndb.FloatProperty(indexed=False)
	
class Order(ndb.Model):
	#represents an order
	id = ndb.StringProperty(indexed=True)
	item = ndb.StructuredProperty(Item)
	user = ndb.StructuredProperty(User)
	cart =ndb.StructuredProperty(Cart)
	totalPrice = ndb.FloatProperty(indexed=False)

def init_products():
	#add products to db
	
	#Check that we haven't already added the book
	products_query = Product.query()
	products = products_query.fetch()

	if len(products) == 0:
		# Open products.xml document using minidom parser
		DOMTree = xml.dom.minidom.parse("resources/products.xml")
		collection = DOMTree.documentElement

		#Get products 
		products = collection.getElementsByTagName("product") 

		# Print detail
		for product in products:
			newproduct = Product(parent=data_store_key(PRODUCTSTORE_NAME))
			
			newproduct.id = product.getAttribute("id");
			
			newproduct.name = name.childNodes[0].data;
			name = product.getElementsByTagName('name')[0]			

			manufacturerId = product.getElementsByTagName('manufacturerId')[0]
			newproduct.manufacturerId = manufacturerId.childNodes[0].data;
									
			price = product.getElementsByTagName('price')[0]	
			newproduct.price = float(price.childNodes[0].data);
						
			stockTotal = product.getElementsByTagName('stockTotal')[0]
			newbook.stockTotal = stockTotal.childNodes[0].data;
								
			newproduct.put();

def init_suppliers():
	"""add to db"""

	#Check that we haven't already added the supplier
	suppliers_query = Supplier.query()
	suppliers = suppliers_query.fetch()

	if len(suppliers) == 0:
		# Open suppliers.xml document using minidom parser
		DOMTree = xml.dom.minidom.parse("resources/suppliers.xml")
		collection = DOMTree.documentElement

		#Get suppliers 
		suppliers = collection.getElementsByTagName("supplier") 

		# Print detail
		for supplier in suppliers:
			newsupplier = Supplier(parent=data_store_key(SUPPLIERSTORE_NAME))
			
			newsupplier.id = supplier.getAttribute("id");
			
			name = supplier.getElementsByTagName('name')[0]
			newsupplier.name = name.childNodes[0].data;
			
			email = supplier.getElementsByTagName('email')[0]
			newsupplier.email = email.childNodes[0].data;
									
			phonenumber = supplier.getElementsByTagName('phonenumber')[0]	
			newsupplier.phonenumber = phonenumber.childNodes[0].data;
						
			url = supplier.getElementsByTagName('url')[0]
			newsupplier.url = url.childNodes[0].data);
								
			newsupplier.put();

def init_items():
	"""add to db"""

	#Check that we haven't already added the item
	items_query = Item.query()
	items = items_query.fetch()

	if len(items) == 0:
		# Open products.xml document using minidom parser
		DOMTree = xml.dom.minidom.parse("resources/items.xml")
		collection = DOMTree.documentElement

		#Get products 
		items = collection.getElementsByTagName("item") 

		# Print detail
		for item in items:
			newitem = Item(parent=data_store_key(ITEMSTORE_NAME))
			
			newitem.id = item.getAttribute("id");
			
			productId = item.getElementsByTagName('productId')[0]
			newitem.productId = productId.childNodes[0].data;
									
			quantity = item.getElementsByTagName('quantity')[0]	
			newitem.quantity = quantity.childNodes[0].data);
							
			newitem.put();


class MainPage(webapp2.RequestHandler):
	"""This is the main handler for our application"""

	def get(self):
		# Checks if the user is logged in
		user = users.get_current_user()

		if user:
			#User is logged in, get his details from user store and db 
			"""Process a HTTP Get Request for the application by returnng the client"""
			template = JINJA_ENVIRONMENT.get_template('page.html')

			template_values = {
				'user_id':user.user_id(),				
				'user_nickname':user.nickname(),
				'logout_url':users.create_logout_url(self.request.uri)}

			self.response.write(template.render(template_values))
		else:
			#User is not logged in so redirect to login page
			self.redirect(users.create_login_url(self.request.uri))


class UserServiceHandler(webapp2.RequestHandler):
	"""This is the user service handler"""

	def get(self,user_id):
		"""Process a HTTP Get Request for the user service by returnng a user"""
		
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
			r['email'] = users[0].email;
			r['address'] = users[0].address;

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
				#user.email = userjson["email"];
				#user.address = userjson["address"];

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
				#user.email = userjson["email"];
				#user.address = userjson["address"];

				#Store the user info
				user.put();
				
				#return a message to the client
				data = {}
				data['message'] = 'Updated User (PUT):'+userjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)
				
				
class SupplierServiceHandler(webapp2.RequestHandler):
	# supplier service handler

	def get(self):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		suppliers_query = Supplier.query()
		suppliers = suppliers_query.fetch()
		
		result = [];
				
		for p in suppliers:
			#store each supplier in a dictionary
			supplier = {}
			supplier['id'] = p.id
			supplier['firstname'] = p.name
			supplier['lastname'] = p.email
			supplier['email'] = p.email
			supplier['phonenumber'] = p.phonenumber
			supplier['url'] = p.url
			
			#add the dictionary to the list
			result.append(supplier);
			
		#Create a new dictionary for the results
		r={};

		#Give the results dictionary a key called suppliers whos value is the list of suppliers returned
		r['suppliers'] = result;
	
		self.response.headers['Content-Type'] = 'text/x-json'
		self.response.write(json.dumps(r, separators=(',',':')))

	
	def put(self):
		#Process a HTTP PUT Request service 
		
		#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#Parse the json we received		
			supplierjson = json.loads(self.request.body)
		
			#check if we already have an entry for that supplier
			suppliers_query = Supplier.query(Supplier.id==supplierjson["id"])
			query_results = suppliers_query.fetch()

			if len(query_results) == 0:
				#We must be adding a new supplier as the query returned zero results
				#Create a new instance of Supplier
				supplier = Supplier(parent=data_store_key(PUBSTORE_NAME))
				supplier.id = supplierjson["id"];
				supplier.name = supplierjson["name"];
				supplier.email = supplierjson["email"];
				supplier.phonenumber = supplierjson["phonenumber"];
				supplier.url = supplierjson["url"];
			
				#Store the supplier info
				supplier.put();

				#return a message to the client
				data = {}
				data['message'] = 'Added Supplier (PUT):'+supplierjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

			else:
				#Update the supplier object
				supplier = query_results[0];
				supplier.name = supplierjson["name"];

				#Store the supplier info
				supplier.put();
		
				#return a message to the client
				data = {}
				data['message'] = 'Updated Supplier (PUT):'+supplierjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self,supplier_id):
		"""Process a HTTP DELETE Request for orders by deleting a order with the specified id"""
		logging.info("Supplier delete called:"+supplier_id)

		#Check that there are no suppliers using this publisher
		suppliers_query = Supplier.query(Supplier.publisher==publisher_id)
		query_results = suppliers_query.fetch()

		if not len(query_results) == 0:
			#We won't allow this publisher to be deleted because there is a supplier entry uning it
			self.error(405) #method not allowed
		else:
			#Checks if the user is logged in
			current_user = users.get_current_user()

		#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#check if we already have an entry for that order
			suppliers_query = Supplier.query(Supplier.id==supplier_id)
			query_results = suppliers_query.fetch()

			if len(query_results) == 0:
				#Resource not found
				self.error(404)
			else:
				#Get the key of the object and deltet it from the key-value data store
				supplier = query_results[0]
				key = supplier.key
				key.delete()
				#return a message to the client
				data = {}
				data['message'] = 'Deleted Supplier:'+supplier_id
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)
								
				
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
			order['item'] = b.item
			order['user'] = b.user			
			order['cart'] = b.cart
			order['totalPrice'] = str(b.totalPrice)

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
			order_query = Order.query(Order.id == orderjson["order"])
			order_query_results = order_query.fetch()
		
			if len(order_query_results)==0:
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
					order.item = orderjson["item"];
					order.user = orderjson["user"];
					order.cart = orderjson["cart"];
					order.totalPrice = float(orderjson["totalPrice"]);
			
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
					order.item = orderjson["item"];
					order.user = orderjson["user"];
					order.cart = orderjson["cart"];
					order.totalPrice = float(orderjson["totalPrice"]);

					#Store the user info
					order.put();
			
					#return a message to the client
					data = {}
					data['message'] = 'Updated Order (PUT):'+orderjson["id"]
					json_response = json.dumps(data)
					self.response.headers['Content-Type'] = 'text/x-json'
					self.response.write(json_response)

					
class ProductServiceHandler(webapp2.RequestHandler):
	# product service handler

	def get(self):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		products_query = Product.query()
		products = products_query.fetch()
		
		result = [];
				
		for p in products:
			#store each product in a dictionary
			product = {}
			product['id'] = p.id
			product['name'] = p.name
			product['manufacturer'] = p.manufacturer
			product['price'] = p.price
			product['stockTotal'] = p.stockTotal
			
			#add the dictionary to the list
			result.append(product);
			
		#Create a new dictionary for the results
		r={};

		#Give the results dictionary a key called products whos value is the list of products returned
		r['products'] = result;
	
		self.response.headers['Content-Type'] = 'text/x-json'
		self.response.write(json.dumps(r, separators=(',',':')))

	
	def put(self):
		#Process a HTTP PUT Request service 
		
	#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#Parse the json we received		
			productjson = json.loads(self.request.body)
		
			#check if we already have an entry for that product
			products_query = Product.query(Product.id==productjson["id"])
			query_results = products_query.fetch()

			if len(query_results) == 0:
				#We must be adding a new product as the query returned zero results
				#Create a new instance of Product
				product = Product(parent=data_store_key(PUBSTORE_NAME))
				product.id = productjson["id"];
				product.name = productjson["name"];
				product.manufacturer = productjson["manufacturer"];
				product.price = productjson["price"];
				product.stockTotal = productjson["stockTotal"];
			
				#Store the product info
				product.put();

				#return a message to the client
				data = {}
				data['message'] = 'Added Product (PUT):'+productjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

			else:
				#Update the product object
				product = query_results[0];
				product.name = productjson["name"];

				#Store the product info
				product.put();
		
				#return a message to the client
				data = {}
				data['message'] = 'Updated Product (PUT):'+productjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self,product_id):
		"""Process a HTTP DELETE Request for orders by deleting a order with the specified id"""
		logging.info("Product delete called:"+product_id)

		#Check that there are no products using this publisher
		products_query = Product.query(Product.publisher==publisher_id)
		query_results = products_query.fetch()

		if not len(query_results) == 0:
			#We won't allow this publisher to be deleted because there is a product entry uning it
			self.error(405) #method not allowed
		else:
			#Checks if the user is logged in
			current_user = users.get_current_user()

		#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#check if we already have an entry for that order
			products_query = Product.query(Product.id==product_id)
			query_results = products_query.fetch()

			if len(query_results) == 0:
				#Resource not found
				self.error(404)
			else:
				#Get the key of the object and deltet it from the key-value data store
				product = query_results[0]
				key = product.key
				key.delete()
				#return a message to the client
				data = {}
				data['message'] = 'Deleted Product:'+product_id
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)
				

class ItemServiceHandler(webapp2.RequestHandler):
	# item service handler

	def get(self):
		#Process a HTTP Get Request for the service 
		
		#Read the data
		items_query = Item.query()
		items = items_query.fetch()
		
		result = [];
				
		for p in items:
			#store each item in a dictionary
			item = {}
			item['id'] = p.id
			item['product'] = p.product
			item['quantity'] = p.quantity
			
			#add the dictionary to the list
			result.append(item);
			
		#Create a new dictionary for the results
		r={};

		#Give the results dictionary a key called items whos value is the list of items returned
		r['items'] = result;
	
		self.response.headers['Content-Type'] = 'text/x-json'
		self.response.write(json.dumps(r, separators=(',',':')))

	
	def put(self):
		#Process a HTTP PUT Request service 
		
	#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#Parse the json we received		
			itemjson = json.loads(self.request.body)
		
			#check if we already have an entry for that item
			items_query = Item.query(Item.id==itemjson["id"])
			query_results = items_query.fetch()

			if len(query_results) == 0:
				#We must be adding a new item as the query returned zero results
				#Create a new instance of Item
				item = Item(parent=data_store_key(PUBSTORE_NAME))
				item.id = itemjson["id"];
				item.product = itemjson["product"];
				item.quantity = itemjson["quantity"];				
			
				#Store the item info
				item.put();

				#return a message to the client
				data = {}
				data['message'] = 'Added Item (PUT):'+itemjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

			else:
				#Update the item object
				item = query_results[0];
				item.name = itemjson["name"];

				#Store the item info
				item.put();
		
				#return a message to the client
				data = {}
				data['message'] = 'Updated Item (PUT):'+itemjson["id"]
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)

	def delete(self,item_id):
		"""Process a HTTP DELETE Request for orders by deleting a order with the specified id"""
		logging.info("Item delete called:"+item_id)

		#Check that there are no items using this publisher
		items_query = Item.query(Item.publisher==publisher_id)
		query_results = items_query.fetch()

		if not len(query_results) == 0:
			#We won't allow this publisher to be deleted because there is a item entry uning it
			self.error(405) #method not allowed
		else:
			#Checks if the user is logged in
			current_user = users.get_current_user()

		#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#check if we already have an entry for that order
			items_query = Item.query(Item.id==item_id)
			query_results = items_query.fetch()

			if len(query_results) == 0:
				#Resource not found
				self.error(404)
			else:
				#Get the key of the object and deltet it from the key-value data store
				item = query_results[0]
				key = item.key
				key.delete()
				#return a message to the client
				data = {}
				data['message'] = 'Deleted Item:'+item_id
				json_response = json.dumps(data)
				self.response.headers['Content-Type'] = 'text/x-json'
				self.response.write(json_response)
				

class CartServiceHandler(webapp2.RequestHandler):
	# service handler

	def get(self):
		"""Process a HTTP Get Request for the order service by returnng all orders"""
		logging.info("cart GET called")

		#Read the order data from the data store
		carts_query = Cart.query()
		carts = carts_query.fetch()
		
		result = [];

		for b in carts:
			#store each order in a dictionary
			cart = {}
			cart['id'] = b.id
			cart['item'] = b.item
			cart['user'] = b.user		
			cart['totalPrice'] = str(b.totalPrice)

			#add the dictionary to the list
			result.append(cart);
			
		#Create a new dictionary for the results
		r={};

		#Give the results dictionary a key called orders whos value is the list of orders returned
		r['carts'] = result;
	
		self.response.headers['Content-Type'] = 'text/x-json'
		self.response.write(json.dumps(r, separators=(',',':')))

	def delete(self,cart_id):
		"""Process a HTTP DELETE Request for orders by deleting a order with the specified id"""
		logging.info("Order delete called:"+order_id)


		#Checks if the user is logged in
		current_user = users.get_current_user()
		
		if not current_user :
			#The request could not be completed because the user is not logged in
			self.error(403) #access denied	
		else:

			#check if we already have an entry for that order
			carts_query = Cart.query(Cart.id==cart_id)
			query_results = carts_query.fetch()

			if len(query_results) == 0:
				#Resource not found
				self.error(404)
			else:
				#Get the key of the object and deltet it from the key-value data store
				cart = query_results[0]
				key = cart.key
				key.delete()
				#return a message to the client
				data = {}
				data['message'] = 'Deleted cart:'+cart_id
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
			cartjson = json.loads(self.request.body)

			#Check if the publisher for the order information exists
			cart_query = Cart.query(Cart.id == cartjson["cart"])
			cart_query_results = cart_query.fetch()
			
			#Read the user data from the data store
			users_query = User.query(User.id==user_id)
			users = users_query.fetch(1)
			
			#check if we already have an entry for that item
			items_query = Item.query(Item.id==itemjson["id"])
			query_results = items_query.fetch()
		
			if len(cart_query_results)==0:
				#There is no publisher in our database with the specified id
				self.error(404); #not found
			else:		

				#check if we already have an entry for that order
				carts_query = Cart.query(Cart.id==cartjson["id"])
				query_results = carts_query.fetch()

				if len(query_results) == 0:
					#We must be adding a new order as the query returned zero results
					#Create a new instance of Order
					cart = Cart(parent=data_store_key(BOOKSTORE_NAME))
					cart.id = cartjson["id"];
					cart.item = cartjson["item"];
					cart.user = cartjson["user"];
					cart.totalPrice = float(cartjson["totalPrice"]);
			
					#Store the user info
					cart.put();

					#return a message to the client
					data = {}
					data['message'] = 'Added cart (PUT):'+cartjson["id"]
					json_response = json.dumps(data)
					self.response.headers['Content-Type'] = 'text/x-json'
					self.response.write(json_response)

				else:
					#Update the cart object
					cart = query_results[0];
					cart.item = cartjson["item"];
					cart.user = cartjson["user"];
					cart.totalPrice = float(cartjson["totalPrice"]);

					#Store the user info
					cart.put();
			
					#return a message to the client
					data = {}
					data['message'] = 'Updated cart (PUT):'+cartjson["id"]
					json_response = json.dumps(data)
					self.response.headers['Content-Type'] = 'text/x-json'
					self.response.write(json_response)

								
				
logging.info("STARTING UP")
#The first time our application runs we want to load book info
init_suppliers();
init_products();
init_items();

application = webapp2.WSGIApplication([
	('/users', UserServiceHandler),
	('/users/(\d+)', UserServiceHandler),
	('/supplier', SupplierServiceHandler),
	('/supplier/(\d+)', SupplierServiceHandler),
	('/order', OrderServiceHandler),
	('/order/(\d+)', OrderServiceHandler),	
	('/product', ProductServiceHandler),
	('/product/(\d+)', ProductServiceHandler),
	('/item', ProductServiceHandler),
	('/item/(\d+)', ProductServiceHandler),
	('/cart', ProductServiceHandler),
	('/cart/(\d+)', ProductServiceHandler),
	], debug=True)


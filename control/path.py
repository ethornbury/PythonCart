import webapp2


path = webapp2.WSGIApplication([
	#user
	(p'/cartservice/control/user',  'control.user.ListHandler'),

	#supplier
	(p'/cartservice/control/supplier',  'control,supplier.SupplierServiceHandler'),
	  
	#product
	(p'/cartservice/control/product',    'control,product.ProductServiceHandler'),
	 
	#item
	(p'/cartservice/control/item',        'control,item.SupplierServiceHandler'),

	#cart
	(p'/cartservice/control/cart',         'control,cart.SupplierServiceHandler'),

	(p'/cartservice/control/.*',            'control,docs.DefaultHandler')
	  
  ])


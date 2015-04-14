/*
Delete a order from our order list
*/
function DeleteOrder(){

	/*Get the order id*/
	var orderId	= document.getElementById("order_id").value.trim();

	if(!orderId){
		alert("ID Required")
	}
	else
	{
	
		var xmlhttp;
		if (window.XMLHttpRequest)
		{// code for IE7+, Firefox, Chrome, Opera, Safari
			xmlhttp=new XMLHttpRequest();
		}
		else
		{// code for IE6, IE5
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		}

		//Create a callback function
		xmlhttp.onreadystatechange=function()
		{
			if(xmlhttp.readyState==4)
			{
				//The call has finished
				if(xmlhttp.status==200)
				{
					//Convert the response into a json object
					response = JSON.parse(xmlhttp.responseText);
					alert(response.message);
				}
				else
				{
					alert('Server returned HTTP status '+xmlhttp.status);
				}

				//refresh the order list
				listOrders();
			}
		}

		//build a json object (only need the id)
		var orderObject ={};
		orderObject.id = orderId;
	
		//Convert JSON object to JSON string
		orderString = JSON.stringify(orderObject);

		//We secify the order ID and we use DELETE instead of POST
		xmlhttp.open("DELETE","/orders/"+orderId,true);
		//xmlhttp.setRequestHeader("Content-type","text/x-json");
		//xmlhttp.send(orderString);
		xmlhttp.send();
	}	
}

/*
Add a order to our order list
*/
function AddOrder(){

	/*Get the first name and last name*/
	var orderId	= document.getElementById("orderId").value.trim();
	var item	= document.getElementById("item").value.trim();
	var user 	= document.getElementById("user").value.trim();
	var cart 	= document.getElementById("cart").value.trim();
	var totalPrice 	= document.getElementById("totalPrice").value.trim();
	

	/*Check that values have been entered*/
	if(!orderId || !itemId	||  !user || !cart || !totalPrice){
		alert("All fields are required");
	}
	else if(!parseFloat(totalPrice)){
		alert("Price must be a floating point number");
	}
	else{

		//Round the price to two decimal places and convert to string
		totalPrice = parseFloat(totalPrice).toFixed(2).toString();

		var xmlhttp;
		if (window.XMLHttpRequest)
		{// code for IE7+, Firefox, Chrome, Opera, Safari
			xmlhttp=new XMLHttpRequest();
		}
		else
		{// code for IE6, IE5
			xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
		}

		//Create a callback function
		xmlhttp.onreadystatechange=function()
		{
			if(xmlhttp.readyState==4)
			{
				//The call has finished
				if(xmlhttp.status==200)
				{
					//Convert the response into a json object
					response = JSON.parse(xmlhttp.responseText);
					alert(response.message);
				}
				else
				{
					alert('Server returned HTTP status '+xmlhttp.status);
				}

				//refresh the order list
				listOrders();
			}
		}

		//build a json object
		var orderObject ={};
		orderObject.id = orderId;
		orderObject.item = item;
		orderObject.user = user;
		orderObject.cart = cart;
		orderObject.totalPrice = totalPrice;

		//Convert JSON object to JSON string
		orderString = JSON.stringify(orderObject);

		//We secify the order ID so we use PUT instead of POST
		xmlhttp.open("PUT","/orders",true);
		xmlhttp.setRequestHeader("Content-type","text/x-json");
		xmlhttp.send(orderString);
	}

}

/*
Make an AJAX claa to retrive a list of orders
*/
function listOrders(){
	var xmlhttp;

	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}

	//Create a callback function
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4)
		{
			if(xmlhttp.status==200)
			{
				//Convert the response into a json object
				var response = JSON.parse(xmlhttp.responseText);
				
				result="<table border='1'><tr><th>ID</th><th>Item Id</th><th>Cart Id</th><th>User Id</th><th>Total</th></tr>"


				for(var i=0;i<response.orders.length;i++){
					
					result+="<tr><td>"+response.orders[i].id
					+"</td><td>"+response.orders[i].item+"</td><td>"
					+response.orders[i].cart+"</td></tr>"
					+response.orders[i].user+"</td></tr>"
					+response.orders[i].totalPrice+"</td></tr>";
					

				}

				result+="</table>"

				document.getElementById("orders").innerHTML = result;
			}
		}
	}

	xmlhttp.open("GET","/orders",true);
	xmlhttp.send();

}


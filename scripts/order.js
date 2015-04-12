/*
Add a order to our order list
*/
function AddOrder(){

	/*Get the first name and last name*/
	var orderId	= document.getElementById("orderId").value.trim();
	var itemId	= document.getElementById("itemId").value.trim();
	var userId 	= document.getElementById("userId").value.trim();
	var cartId 	= document.getElementById("cartId").value.trim();
	var totalPrice 	= document.getElementById("totalPrice").value.trim();
	

	/*Check that values have been entered*/
	if(!orderId || !itemId	||  !userId || !cartId || !totalPrice){
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
		orderObject.itemId = itemId
		orderObject.userId = userId;
		orderObject.cartId = cartId;
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
					+"</td><td>"+response.orders[i].itemId+"</td><td>"
					+response.orders[i].cartId+"</td></tr>"
					+response.orders[i].userId+"</td></tr>"
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


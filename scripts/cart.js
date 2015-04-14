/*
Delete a cart from our cart list
*/
function DeleteCart(){

	/*Get the cart id*/
	var cartId	= document.getElementById("cart_id").value.trim();

	if(!cartId){
		alert("cart ID Required")
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

				//refresh the cart list
				listcarts();
			}
		}

		//build a json object (only need the id)
		var cartObject ={};
		cartObject.id = cartId;
	
		//Convert JSON object to JSON string
		cartString = JSON.stringify(cartObject);

		//We secify the cart ID and we use DELETE instead of POST
		xmlhttp.open("DELETE","/carts/"+cartId,true);
		//xmlhttp.setRequestHeader("Content-type","text/x-json");
		//xmlhttp.send(cartString);
		xmlhttp.send();
	}	
}
/*
Add a cart to our cart list
*/
function AddCart(){

	/*Get the first name and last name*/
	var cartId	= document.getElementById("cart_id").value.trim();
	var item 	= document.getElementById("item").value.trim();
	var user 	= document.getElementById("user").value.trim();
	var totalPrice 	= document.getElementById("totalPrice").value.trim();
	

	/*Check that values have been entered*/
	if(!cartId || !item ||  !user || !totalPrice){
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

				//refresh the cart list
				listCarts();
			}
		}

		//build a json object
		var cartObject ={};
		cartObject.id = cartId;
		cartObject.item = item;
		cartObject.user = user;
		cartObject.totalPrice = totalPrice;

		//Convert JSON object to JSON string
		cartString = JSON.stringify(cartObject);

		//We secify the cart ID so we use PUT instead of POST
		xmlhttp.open("PUT","/carts",true);
		xmlhttp.setRequestHeader("Content-type","text/x-json");
		xmlhttp.send(cartString);
	}

}

/*
Make an AJAX claa to retrive a list of carts
*/
function listCarts(){
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
				
				result="<table border='1'><tr><th>ID</th><th>Item Id</th><th>User Id</th><th>Total Price</th></tr>"


				for(var i=0;i<response.carts.length;i++){
					
					result+="<tr><td>"+response.carts[i].id
					+"</td><td>"+response.carts[i].item+"</td><td>"
					+response.carts[i].user+"</td></tr>"
					+response.carts[i].totalPrice+"</td></tr>";
					
				}

				result+="</table>"

				document.getElementById("carts").innerHTML = result;
			}
		}
	}

	xmlhttp.open("GET","/carts",true);
	xmlhttp.send();

}


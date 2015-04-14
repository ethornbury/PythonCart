/*
Delete a item from our item list
*/
function DeleteItem(){

	/*Get the item id*/
	var itemId	= document.getElementById("book_id").value.trim();

	if(!bookId){
		alert("Item ID Required")
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

				//refresh the item list
				listItems();
			}
		}

		//build a json object (only need the id)
		var itemObject ={};
		itemObject.id = itemId;
	
		//Convert JSON object to JSON string
		itemString = JSON.stringify(itemObject);

		//We secify the item ID and we use DELETE instead of POST
		xmlhttp.open("DELETE","/items/"+itemId,true);
		//xmlhttp.setRequestHeader("Content-type","text/x-json");
		//xmlhttp.send(bookString);
		xmlhttp.send();
	}	
}
/*
Add a item to our item list
*/
function AddItem(){

	/*Get the first name and last name*/
	var itemId	= document.getElementById("item_id").value.trim();
	var productId 	= document.getElementById("product").value.trim();
	var quantity 	= document.getElementById("quantity").value.trim();

	/*Check that values have been entered*/
	if(!itemId || !itemId ||  !product || !quantity){
		alert("All fields are required");
	}
	
	else{

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

				//refresh the item list
				listItems();
			}
		}

		//build a json object
		var itemObject ={};
		itemObject.id = itemId;
		itemObject.product = product;
		itemObject.quantity = quantity;

		//Convert JSON object to JSON string
		itemString = JSON.stringify(itemObject);

		//We secify the item ID so we use PUT instead of POST
		xmlhttp.open("PUT","/items",true);
		xmlhttp.setRequestHeader("Content-type","text/x-json");
		xmlhttp.send(itemString);
	}

}

/*
Make an AJAX claa to retrive a list of items
*/
function listItems(){
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
				
				result="<table border='1'><tr><th>ID</th><th>Product Id</th><th>Quantity</th></tr>"


				for(var i=0;i<response.items.length;i++){
					
					result+="<tr><td>"+response.items[i].id
					+"</td><td>"+response.items[i].product+"</td><td>"
					+response.items[i].quantity+"</td></tr>";				

				}

				result+="</table>"

				document.getElementById("items").innerHTML = result;
			}
		}
	}

	xmlhttp.open("GET","/items",true);
	xmlhttp.send();

}


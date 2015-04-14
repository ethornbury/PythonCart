/*
Add a product to our product list
*/
function AddProduct(){

	/*Get the first name and last name*/
	var product	= document.getElementById("product_id").value.trim();
	var name 	= document.getElementById("name").value.trim();
	var manufacturer 	= document.getElementById("manufacturer_id").value.trim();
	var price 	= document.getElementById("price").value.trim();
	var stockTotal 	= document.getElementById("stockTotal").value.trim();

	/*Check that values have been entered*/
	if(!productId || !name ||  !manufacturer_id || !price || !stockTotal){
		alert("All fields are required");
	}
	else if(!parseFloat(price)){
		alert("Price must be a floating point number");
	}
	else{

		//Round the price to two decimal places and convert to string
		price = parseFloat(price).toFixed(2).toString();

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

				//refresh the product list
				listProducts();
			}
		}

		//build a json object
		var productObject ={};
		productObject.id = productId;
		productObject.name = name;
		productObject.manufacturer = manufacturerId;
		productObject.price = price;
		productObject.stockTotal = stockTotal;

		//Convert JSON object to JSON string
		productString = JSON.stringify(productObject);

		//We secify the product ID so we use PUT instead of POST
		xmlhttp.open("PUT","/products",true);
		xmlhttp.setRequestHeader("Content-type","text/x-json");
		xmlhttp.send(productString);
	}

}

/*
Make an AJAX claa to retrive a list of products
*/
function listProducts(){
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
				
				result="<table border='1'><tr><th>ID</th><th>Name</th><th>Manufacturer Id</th><th>Price</th><th>Stock Total</th></tr>"


				for(var i=0;i<response.products.length;i++){
					
					result+="<tr><td>"+response.products[i].id
					+"</td><td>"+response.products[i].name+"</td><td>"
					+response.products[i].manufacturer+"</td></tr>"
					+response.products[i].price+"</td></tr>"
					+response.products[i].stockTotal+"</td></tr>";
					

				}

				result+="</table>"

				document.getElementById("products").innerHTML = result;
			}
		}
	}

	xmlhttp.open("GET","/products",true);
	xmlhttp.send();

}


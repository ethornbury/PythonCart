/*
Add a supplier to our supplier list
*/
function AddSupplier(){

	/*Get the first name and last name*/
	var supplierId	= document.getElementById("supplier_id").value.trim();
	var nameSupplier 	= document.getElementById("nameSupplier").value.trim();
	var email 	= document.getElementById("email").value.trim();
	var phonenumber 	= document.getElementById("phonenumber").value.trim();
	var url 	= document.getElementById("url").value.trim();

	/*Check that values have been entered*/
	if(!supplierId || !nameSupplier ||  !email || !phonenumber || !url){
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

				//refresh the supplier list
				listSuppliers();
			}
		}

		//build a json object
		var supplierObject ={};
		supplierObject.id = supplierId;
		supplierObject.nameSupplier = nameSupplier;
		supplierObject.email = email;
		supplierObject.phonenumber = phonenumber;
		supplierObject.url = url;

		//Convert JSON object to JSON string
		supplierString = JSON.stringify(supplierObject);

		//We secify the supplier ID so we use PUT instead of POST
		xmlhttp.open("PUT","/suppliers",true);
		xmlhttp.setRequestHeader("Content-type","text/x-json");
		xmlhttp.send(supplierString);
	}

}

/*
Make an AJAX claa to retrive a list of suppliers
*/
function listSuppliers(){
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
				
				result="<table border='1'><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone Number</th><th>URL</th></tr>"


				for(var i=0;i<response.suppliers.length;i++){
					
					result+="<tr><td>"+response.suppliers[i].id
					+"</td><td>"+response.suppliers[i].nameSupplier+"</td><td>"
					+response.suppliers[i].email+"</td></tr>"
					+response.suppliers[i].phonenumber+"</td></tr>"
					+response.suppliers[i].url+"</td></tr>";
					

				}

				result+="</table>"

				document.getElementById("suppliers").innerHTML = result;
			}
		}
	}

	xmlhttp.open("GET","/suppliers",true);
	xmlhttp.send();

}


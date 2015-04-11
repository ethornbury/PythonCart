var userDetailsStored = false;


/*Function to add a user with an ajax post call*/
function updateUserDetails(){

	/*Get the first name and last name*/
	var userId		= document.getElementById("userid").innerHTML;
	var firstName 	= document.getElementById("firstname").value.trim();
	var lastName 	= document.getElementById("lastname").value.trim();

	/*Check that values have been entered*/
	if(!firstName || !lastName){
		alert("All fields are required");
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
					userDetailsStored = true;
					response = JSON.parse(xmlhttp.responseText);
					alert(response.message);
				}
				else
				{
					alert('Server returned HTTP status '+xmlhttp.status);
				}
			}
		}

		//build a json object
		var userObject ={};
		userObject.id = userId;
		userObject.firstName = firstName;
		userObject.lastName = lastName;

		//Convert JSON object to JSON string
		userString = JSON.stringify(userObject);

		if(userDetailsStored){
			//If user details have previously been stored we are doing a put to update
			xmlhttp.open("PUT","/users",true);
			xmlhttp.setRequestHeader("Content-type","text/x-json");
			xmlhttp.send(userString);
		}else{
			//If user details have not previously been stored we are doing a post to create
			xmlhttp.open("POST","/users",true);
			xmlhttp.setRequestHeader("Content-type","text/x-json");
			xmlhttp.send(userString);

		}
	}
}



function getUser(){

	//Create an object to make AJAX requests for us	
	var xmlhttp;

	if (window.XMLHttpRequest)
	{// code for IE7+, Firefox, Chrome, Opera, Safari
		xmlhttp=new XMLHttpRequest();
	}
	else
	{// code for IE6, IE5
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}

	//Create a callback function to handle the result of the AJAX call
	xmlhttp.onreadystatechange=function()
	{
		if(xmlhttp.readyState==4)
		{
			if(xmlhttp.status==200)
			{
				//Notice that we are trusting that the server sent us back the right user info
				//We could check the id attribute of the response to make sure

				//Convert the response into a json object
				var response = JSON.parse(xmlhttp.responseText);
				
				if(response.firstname.trim().length > 0 && response.lastname.trim().length > 0){
					userDetailsStored = true;

					//Set the first and last names of the user in our form inputs
					document.getElementById("firstname").value = response.firstname;
					document.getElementById("lastname").value = response.lastname;
				}
			}
		}
	}


	//Get the user id
	idquery = document.getElementById('userid').innerHTML.trim();
	xmlhttp.open("GET","/users/"+idquery,true);
	xmlhttp.send();

}



/*
Add a book to our book list
*/
function AddBook(){

	/*Get the first name and last name*/
	var bookId	= document.getElementById("book_id").value.trim();
	var title 	= document.getElementById("title").value.trim();
	var author 	= document.getElementById("author").value.trim();
	var price 	= document.getElementById("price").value.trim();

	/*Check that values have been entered*/
	if(!bookId || !title || !author || !price){
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

				//refresh the book list
				listBooks();
			}
		}

		//build a json object
		var bookObject ={};
		bookObject.id = bookId;
		bookObject.author = author;
		bookObject.title = title;
		bookObject.price = price;

		//Convert JSON object to JSON string
		bookString = JSON.stringify(bookObject);

		//We secify the book ID so we use PUT instead of POST
		xmlhttp.open("PUT","/books",true);
		xmlhttp.setRequestHeader("Content-type","text/x-json");
		xmlhttp.send(bookString);
	}

}

/*
Make an AJAX claa to retrive a list of books
*/
function listBooks(){
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
				
				result="<table border='1'><tr><th>ID</th><th>Title</th><th>Author</th><th>Price</th></tr>"


				for(var i=0;i<response.books.length;i++){
					
					result+="<tr><td>"+response.books[i].id+"</td><td>"+response.books[i].title+"</td><td>"+response.books[i].author+"</td><td>"+response.books[i].price+"</td></tr>";
					

				}

				result+="</table>"

				document.getElementById("books").innerHTML = result;
			}
		}
	}

	xmlhttp.open("GET","/books",true);
	xmlhttp.send();

}


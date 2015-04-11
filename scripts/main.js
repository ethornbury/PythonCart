
/*Function to initialise the user interface*/
function initUI(){

	//Fill in the current users details if they are available
	getUser();

	/*LIst alll available books*/
	listBooks();
}

//Get the user info when the page loads
window.onLoad = initUI();

function cl(s) {
	console.log(s);
}

function byId(id) {
	return document.getElementById(id);
}

function httpPost() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			cl('inside')
		}
	};
	xhttp.open("POST", "/checkup", true);
	xhttp.send();
}

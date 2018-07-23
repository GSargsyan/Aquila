function cl(s) {
	console.log(s);
}

function byId(id) {
	return document.getElementById(id);
}

function httpPost(url, payload, callback) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			if (callback) callback(JSON.parse(this.response));
		}
	};
	
	xhttp.open('POST', url);
	xhttp.setRequestHeader("Content-Type", "application/json");
	xhttp.send(JSON.stringify(payload));
}

function newElem(tag) {
	return document.createElement(tag);
}

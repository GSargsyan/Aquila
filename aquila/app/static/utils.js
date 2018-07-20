function cl(s) {
	console.log(s);
}

function byId(id) {
	return document.getElementById(id);
}

function httpPost(url, payload, callback, method, async) {
	if (method === undefined)
		method = 'POST';
	if (async === undefined)
		async = true;

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			if (callback) callback(this.response);
		}
	};
	
	xhttp.open(method, url, async);
	xhttp.send(JSON.stringify(payload));
}

function newElem(tag) {
	return document.createElement(tag);
}

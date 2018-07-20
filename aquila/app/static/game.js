function checkup(response) {
	respObj = JSON.parse(response)
	if (respObj.status != 1) {
		return;
	}
	byId('till-round-start').innerHTML = respObj.left;
}

function logout() {
	httpPost('/logout');
}

function bet() {
	dataObj = {'str-1': 1, 'red': 1};
	httpPost('/bet', JSON.stringify(dataObj), '', 'POST', true, true);
}

window.setInterval(function() { httpPost('/checkup', '', checkup); }, 1000);

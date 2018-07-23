function checkup(response) {
	if (response.status != 1) {
		return;
	}
	byId('till-round-start').innerHTML = response.left;
}

function logout() {
	httpPost('/logout');
}

function bet() {
	dataObj = {'str-1': 1, 'red': 1};
	httpPost('/bet', JSON.stringify(dataObj));
}

window.setInterval(function() { httpPost('/checkup', '', checkup); }, 1000);

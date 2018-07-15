function checkup(response) {
	cl(response);
	if (response.status != 1) {
		return;
	}
	byId('till_round_start').innerHTML = response.left;
}

function logout() {
	httpPost('/logout');
}

window.setInterval(function() { httpPost('/checkup', '', checkup); }, 1000);

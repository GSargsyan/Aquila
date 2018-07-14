function requestRoomInit() {
}

function checkup() {
	httpPost('/checkup', '');
}

function logout() {
	httpPost('/logout');
}

// window.setInterval(checkup, 5000);

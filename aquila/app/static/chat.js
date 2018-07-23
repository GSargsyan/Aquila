// INIT CHAT \\
var token;
var socket;

httpPost('/get_token', '', connectToSocket);

function connectToSocket(response) {
	if (response.status != 1) {
		return;
	}
	token = response.token;
	socket = io('http://localhost:3000', {query: 'token=' + token});

	socket.on('msg', function (msg) {
		chatMessages = byId('chat-messages');
		msgElem = newElem('p');
		msgElem.innerHTML = msg;
		chatMessages.appendChild(msgElem);
	});
}
// END INITING CHAT \\

function checkSubmit(event) {
	if (event.keyCode === 13) { // If enter was preseed
		inputElem = byId('chat-input');
		msg = inputElem.value;
		if (msg != "" || msg != "\n") {
			inputElem.value = '';
			sendMsg(msg);
		}
	}
}

function sendMsg(msg) {
	if (!socket)
		return;
	socket.emit('msg', msg);
}

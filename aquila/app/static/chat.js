var socket = io('http://localhost:3000');

socket.on('msg', function (msg) {
	chatMessages = byId('chat-messages');
	msgElem = newElem('p');
	msgElem.innerHTML = msg;
	chatMessages.appendChild(msgElem);
});

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
	socket.emit('msg', msg);
}

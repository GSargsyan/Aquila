var io = require('socket.io').listen(3000);

io.on('connection', function(socket) {
	console.log('A user connected');

	socket.join('chatters');
	socket.on('msg', function(data) {
		io.to('chatters').emit('msg', data);
	});
});

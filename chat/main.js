function cl(data) {
	console.log(data);
}

var pg = require('pg');
var conString = "postgres://aquila:aquila2018@localhost:5432/aquila";

var config = {
	    user: 'aquila',
	    database: 'aquila',
	    password: 'aquila2018',
	    host: 'localhost',
	    port: 5432,
	    max: 10, // max number of clients in the pool
	    idleTimeoutMillis: 30000
};

var client = new pg.Client(conString);
client.connect();

function dbSelect(callback, fields, table, where, limit) {
	q = "SELECT " + fields + " FROM " + table + " WHERE " + where;
	if (limit) {
		q += " LIMIT " + limit.toString();
	}

	client.query(q, (err, res) => {
		if (!res || !res.rows[0].room_id)
			return;
		callback(res.rows);
	});
}

function connectCallback(socket) {
	token = socket.handshake.query.token;
	if (!token)
		return;

	dbSelect(function(res) {
		roomId = res[0].room_id.toString();
		socket.roomId = roomId;
		socket.join('room-' + roomId);
		socket.roomId = roomId;
		socket.on('msg', function(msg) {
			io.to('room-' + socket.roomId).emit('msg', msg);
		});
	}, 'room_id', 'players', "token='" + token + "'", 1);
}

var io = require('socket.io').listen(3000);
io.on('connection', function(socket) {
	connectCallback(socket);
});

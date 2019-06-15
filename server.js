var WebSocketServer = require('ws').Server
, wss = new WebSocketServer({port: 8124})
, var today = new Date();
wss.on('connection', function(ws) {
　　ws.on('message', function(message) {
　　console.log('received: %s', message);
});
ws.send(today);
//ws.send('something');
});

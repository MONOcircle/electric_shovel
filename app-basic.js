var app = require('http').createServer(handler)
var io = require('socket.io').listen(app);
var fs = require('fs');
 
app.listen(9999);
 
function handler (req, res) {
  fs.readFile(__dirname + '/index.html',
  function (err, data) {
    if (err) {
      res.writeHead(500);
      return res.end('Error loading index.html');
    }
 
    res.writeHead(200);
    res.end(data);
  });
}
 
//接続イベントで
io.sockets.on('connection', function (socket) {
//ferret イベントで　 tobiを受信し、wootをackとしてクライアントに送信
socket.on('ferret', function (name, fn) {
    fn('TomoSoft');
  });
});
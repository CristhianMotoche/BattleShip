export function regiterToPorts(ports) {
  ports.wsConnect.subscribe(function(path){
    var ws = new WebSocket(path);

    ws.onerror = function (event) {
      ports.wsError.send("ERROR");
      console.log("ERROR!");
      ws.close();
    }

    ws.onmessage = function(message) {
      ports.wsIn.send(message.data);
    };

    ports.wsOut.subscribe(function(msg) {
      ws.send(msg);
    });
  });
};

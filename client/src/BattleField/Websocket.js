export function regiterToPorts(ports) {
  ports.wsConnect.subscribe(function(path){
    var ws = new WebSocket(path);

    ws.onerror = function (event) {
      ports.wsError.send(JSON.stringify({data:"ERROR",timeStamp:event.timeStamp}));
    }

    ws.onmessage = function(message) {
      ports.wsIn.send(JSON.stringify({data:message.data,timeStamp:message.timeStamp}));
    };

    ports.wsOut.subscribe(function(msg) {
      ws.send(msg);
    });
  });
};

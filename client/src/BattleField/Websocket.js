export function regiterToPorts(ports) {
  ports.wsConnect.subscribe(function(path){
    var ws = new WebSocket(path);
    ws.onmessage = function(message)
    {
      console.log(message);
      ports.wsIn.send(JSON.stringify({data:message.data,timeStamp:message.timeStamp}));

    };
    ports.wsOut.subscribe(function(msg) { ws.send(msg);  });
  });
};

export function regiterToPorts(ports) {
  ports.wsConnect.subscribe(function(session_id){
    var ws = new WebSocket(`ws://127.0.0.1:5000/ws/${session_id}`);
    ws.onmessage = function(message)
    {
      console.log(message);
      ports.wsIn.send(JSON.stringify({data:message.data,timeStamp:message.timeStamp}));

    };
    ports.wsOut.subscribe(function(msg) { ws.send(msg);  });
  });
};

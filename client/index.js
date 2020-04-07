import './sass/main.scss'

if (module.hot) {
  module.hot.dispose(() => {
    window.location.reload();
  });
}

import('./src/Main.elm')
  .then(({ Elm }) => {
    var node = document.querySelector('main');
    Elm.Main.init({ node: node });

    var app = Elm.Main.init({node: document.getElementById("elm-node")});
    app.ports.websocketConnect.subscribe(function(session_id){
      var ws = new WebSocket(`ws://127.0.0.1:5000/ws/${session_id}`);
      ws.onmessage = function(message)
      {
        console.log(message);
        app.ports.websocketIn.send(JSON.stringify({data:message.data,timeStamp:message.timeStamp}));

      };
      app.ports.websocketOut.subscribe(function(msg) { ws.send(msg);  });
    });
  });

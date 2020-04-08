import './sass/main.scss'
import { regiterToPorts } from './src/BattleField/Websocket.js';

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
    regiterToPorts(app.ports);
  });

port module BattleField.Websocket exposing (wsIn, wsOut, wsError, wsConnect)

port wsIn : (String -> msg) -> Sub msg
port wsOut : String -> Cmd msg
port wsError : (String -> msg) -> Sub msg
port wsConnect : String -> Cmd msg

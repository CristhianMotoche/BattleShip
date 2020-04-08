port module BattleField.Websocket exposing (wsIn, wsOut, wsConnect)

port wsIn : (String -> msg) -> Sub msg
port wsOut : String -> Cmd msg
port wsConnect : Int -> Cmd msg

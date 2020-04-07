port module BattleField.Index exposing (Model, Msg(..), init, view, update, getKey, wsin, wsConnect)


import Html as H
import Html.Attributes as HA
import Html.Events as HE
import Browser.Navigation as Nav

import BattleField.Route as R


-- JavaScript usage: app.ports.websocketIn.send(response);
--port websocketIn : (String -> msg) -> Sub msg
-- JavaScript usage: app.ports.websocketOut.subscribe(handler);
port websocketOut : String -> Cmd msg
port websocketConnect : Int -> Cmd msg


type alias Model =
  { title : Maybe String
  , body : ()
  , key : Nav.Key
  , msg : String
  }

init : Nav.Key -> Model
init key =
  { title = Nothing
  , body = ()
  , key = key
  , msg = "Nothing yet..."
  }

type Msg = Submit | WSIn String | WSConnect Int

wsin = WSIn

wsConnect = WSConnect

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Submit -> (model, websocketOut "Hello")
    WSIn str -> ({model | msg = str}, websocketOut "Hello")
    WSConnect int -> (model, websocketConnect int)


getKey : Model -> Nav.Key
getKey model = model.key


view : Model -> H.Html Msg
view model =
  H.div
    [ HA.class "index" ]
    [ H.div [ HA.class "index__title" ]
            [ H.h1 []
                   [H.text "BattleField"]],

      H.div [][ H.text model.msg ],

      H.div [ HA.class "index__play" ]
            [ H.a [ HA.href (R.toString R.Sessions), HA.class "button" ]
                  [ H.text "Play" ]
            , H.a [ HA.href "somewhere", HA.class "button" ]
                  [ H.text "Scores"]
            , H.button [ HE.onClick Submit, HA.class "button" ]
                       [ H.text "Send" ]
            , H.button [ HE.onClick (WSConnect 1), HA.class "connect" ]
                       [ H.text "Connect" ]
            , H.button [ HE.onClick (WSConnect 2), HA.class "connect" ]
                       [ H.text "Connect" ]
            ]
    ]

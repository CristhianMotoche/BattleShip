module BattleField.Index exposing (Model, Msg(..), init, view, update, getKey, wsin, wsIndexConnect)


import Html as H
import Html.Attributes as HA
import Html.Events as HE
import Browser.Navigation as Nav

import BattleField.Route as R
import BattleField.Websocket exposing (wsOut, wsConnect)


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

wsIndexConnect = WSConnect

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Submit -> (model, wsOut "Hello")
    WSIn str -> ({model | msg = str}, wsOut "Hello")
    WSConnect int -> (model, wsConnect int)


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

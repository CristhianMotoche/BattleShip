module BattleField.Game exposing (Model, Msg, getKey, init, view, update, subs)

import Html as H
import Html.Events as HE
import Html.Attributes as HA

import Browser.Navigation as Nav

import BattleField.Websocket as WS
import BattleField.Route as BR


type alias Model =
  { key : Nav.Key
  , title : Maybe String
  , msg : String
  }

size : Int
size = 10

subs : Model -> Sub Msg
subs _ = WS.wsIn WSIn

type Msg =
  WSIn String
  | WSOut String

init : Nav.Key -> Int -> (Model, Cmd Msg)
init key sessionId =
  ({ key = key
   , title = Just "Game"
   , msg = "Waiting..."
   }
  , WS.wsConnect (BR.wsURL <| BR.Session sessionId)
  )

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    WSIn str -> ({model | msg = str}, Cmd.none)
    WSOut str -> (model, WS.wsOut str)

getKey : Model -> Nav.Key
getKey model = model.key

view : Model -> H.Html Msg
view model =
  H.div
    []
    [ H.text model.msg
    , boardView
    , boardView
    , H.button [ HE.onClick (WSOut "Hello!") ]
               [ H.text "Send hello!" ]
    ]


boardView : H.Html msg
boardView =
  H.div
    [ HA.class "board" ]
    <| List.repeat (size * size) squareView


squareView : H.Html msg
squareView =
  H.div [ HA.class "square" ] []

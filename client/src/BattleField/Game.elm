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

type alias Board = List Square
type alias Square = (String, Int)

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
    , boardView board
    , boardView board
    , H.button [ HE.onClick (WSOut "Hello!") ]
               [ H.text "Send hello!" ]
    ]


board : Board
board =
  let
      alphas = String.split "" "ABCDEFGHIJ"
      nums = List.range 1 size
  in
     List.concatMap (\x -> List.map (\y -> (x, y)) nums) alphas

alphaIndexView : List (H.Html msg)
alphaIndexView =
  let
     singleAlphaView letter = H.div [][ H.text letter ]
  in
     List.map singleAlphaView <| String.split "" "ABCDEFGHIJ"


boardView : Board -> H.Html msg
boardView b =
  H.div [ HA.class "board" ]
        <| List.map squareView b


squareView : Square -> H.Html msg
squareView (c, i) =
  H.div [ HA.class "square" ]
        [ H.text <| c ++ String.fromInt i]

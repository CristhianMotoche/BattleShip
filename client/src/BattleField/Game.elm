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

type alias Board = List (List Square)
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



nums = List.range 1 size

board : Board
board =
  let
      alphas = String.split "" "ABCDEFGHIJ"
  in
     List.map (\x -> List.map (\y -> (x, y)) nums) alphas

alphaIndexView : List (H.Html msg)
alphaIndexView =
  let
     singleAlphaView letter = H.div [][ H.text letter ]
  in
     List.map singleAlphaView <| String.split "" "XABCDEFGHIJ"

numsIndexView : List (H.Html msg)
numsIndexView =
  let
     singleAlphaView num = H.div [][ H.text <| String.fromInt num ]
  in
     List.map singleAlphaView <| List.range 1 size


boardView : Board -> H.Html msg
boardView b =
  H.div [ HA.class "board" ]
        <| List.append alphaIndexView
        <| List.concatMap indexSquareView (zip nums b)

indexSquareView : (Int, List Square) -> List (H.Html msg)
indexSquareView (idx, squares) =
  H.div [ HA.class "num" ][ H.text <| String.fromInt idx ]
  :: List.map squareView squares

squareView : Square -> H.Html msg
squareView (c, i) =
  H.div [ HA.class "square" ]
        [ H.text <| c ++ String.fromInt i]


zip : List a -> List b -> List (a, b)
zip la lb =
  case (la, lb) of
    ([], []) -> []
    ([], _) -> []
    (_, []) -> []
    (a::as_, b::bs) -> (a, b) :: zip as_ bs

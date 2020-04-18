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
  , ourBoard : Board
  , theirBoard : Board
  }

size : Int
size = 10

type alias Board = List (List Square)
type alias Pos = (String, Int)
type alias Square =
  { pos : Pos
  , usedByBoat : Bool
  }

subs : Model -> Sub Msg
subs _ = WS.wsIn WSIn

type Msg =
  WSIn String
  | WSOut String
  | SetBoatHead Pos
  | SetBoatTail Pos

init : Nav.Key -> Int -> (Model, Cmd Msg)
init key sessionId =
  ({ key = key
   , title = Just "Game"
   , msg = "Waiting..."
   , ourBoard = initBoard
   , theirBoard = initBoard
   }
  , WS.wsConnect (BR.wsURL <| BR.Session sessionId)
  )

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    WSIn str -> ({model | msg = str}, Cmd.none)
    WSOut str -> (model, WS.wsOut str)
    SetBoatHead pos ->
        ({ model | ourBoard = setBoatHead pos initBoard}, Cmd.none)
    SetBoatTail square -> (model, Cmd.none)


setBoatHead : Pos -> Board -> Board
setBoatHead pos board =
  List.indexedMap
    (\_ squareList ->
      List.indexedMap
        (\_ square ->
            if square.pos == pos
            then { square | usedByBoat = True }
            else square
        ) squareList
    ) board

getKey : Model -> Nav.Key
getKey model = model.key

view : Model -> H.Html Msg
view model =
  H.div
    []
    [ H.text model.msg
    , H.div [ HA.class "us" ]
            [ boardView  model.ourBoard ]
    , H.div [ HA.class "them" ][ boardView  model.theirBoard ]
    , H.button [ HE.onClick (WSOut "Hello!") ]
               [ H.text "Send hello!" ]
    ]


alphas = String.split "" "ABCDEFGHIJ"
nums = List.range 1 size

initBoard : Board
initBoard =
  let
      toSquare pos =
        { pos = pos
        , usedByBoat = False
        }
  in
    List.map (\x -> List.map (\y -> toSquare (x, y)) nums) alphas

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


boardView : Board -> H.Html Msg
boardView b =
  H.div [ HA.class "board" ]
    <| List.append (letterView "X" :: List.map numView nums)
    <| List.concatMap alphaSquareView (List.map2 Tuple.pair alphas b)

letterView : String -> H.Html msg
letterView letter = H.div [ HA.class "letter" ][ H.text letter ]

numView : Int -> H.Html ms
numView idx = H.div [ HA.class "num" ][ H.text <| String.fromInt idx ]

alphaSquareView : (String, List Square) -> List (H.Html Msg)
alphaSquareView (letter, squares) =
  letterView letter :: List.map squareView squares

squareView : Square -> H.Html Msg
squareView {pos, usedByBoat} =
  let
      (c, i) = pos
  in
    H.div [ HA.class "square"
          , if usedByBoat
            then HA.class "used-by-boat"
            else HA.class ""
          , HE.onClick (SetBoatHead pos)
          ]
          [ H.text <| c ++ String.fromInt i ]

module BattleField.Game exposing (Model, Msg, getKey, init, view, update, subs)

import Html as H
import Html.Events as HE
import Html.Attributes as HA

import Browser.Navigation as Nav

import List.Extra as LE

import BattleField.Websocket as WS
import BattleField.Route as BR


type alias Model =
  { key : Nav.Key
  , title : Maybe String
  , msg : String
  , placingError : Maybe PlacingError
  , ourBoard : Board
  , theirBoard : Board
  , headShip : Maybe Pos
  , tailShip : Maybe Pos
  , phase : Phase
  }

type PlacingError =
  TooLarge | TooSmall | NotInAxis | AlreadyUsed

type Phase = PlacingBoats | Playing


placingErrorToText : PlacingError -> String
placingErrorToText  err =
  case err of
    TooLarge -> "That position is too far"
    TooSmall -> "That position is too close"
    NotInAxis -> "That position is not in the right axis"
    AlreadyUsed -> "Position already used"

size : Int
size = 10

type alias Board = List (List Square)
type alias Pos = (String, Int)
type alias Square =
  { pos : Pos
  , usedByBoat : Bool
  }
type alias Cans =
  { canSetTail : Bool
  , canSetHead : Bool
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
   , placingError = Nothing
   , ourBoard = initBoard
   , theirBoard = initBoard
   , headShip = Nothing
   , tailShip = Nothing
   , phase = PlacingBoats
   }
  , WS.wsConnect (BR.wsURL <| BR.Session sessionId)
  )

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    WSIn str -> ({model | msg = str}, Cmd.none)
    WSOut str -> (model, WS.wsOut str)
    SetBoatHead pos ->
        ({ model | ourBoard = setBoatHead pos model.ourBoard, headShip = Just pos},
        Cmd.none)
    SetBoatTail pos ->
      case model.headShip of
        Just headPos ->
          case positionAvailable (headPos, pos) model.ourBoard of
            Just err -> ({ model | placingError = Just err }, Cmd.none)
            Nothing ->
              ({ model |
                 ourBoard = setBoatTail (headPos, pos) model.ourBoard
               , tailShip = Just pos
               , placingError = Nothing
               }, Cmd.none)
        Nothing ->
              (model, Cmd.none)


positionAvailable : (Pos, Pos) -> Board -> Maybe PlacingError
positionAvailable (headPos, tailPos) board =
  let
      squares = List.concat board
      ((hi, hj), (ti, tj)) = (headPos, tailPos)
  in
       if hi == ti || hj == tj then
         Nothing
       else
         Just NotInAxis


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

setBoatTail : (Pos, Pos) -> Board -> Board
setBoatTail positions board =
  List.indexedMap
    (\_ squareList ->
      List.indexedMap
        (\_ square ->
            if memberInLine square.pos positions
            then { square | usedByBoat = True }
            else square
        ) squareList
    ) board


memberInLine : Pos -> (Pos, Pos) -> Bool
memberInLine (ai, aj) (h, t) =
  let
      (mxi, mxj) = max h t
      (mni, mnj) = min h t
      rangei = LE.dropWhile (\a -> a /= mni) <| LE.dropWhileRight (\a -> a /= mxi) alphas
      rangej = LE.dropWhile (\a -> a /= mnj) <| LE.dropWhileRight (\a -> a /= mxj) nums
  in
    List.member ai rangei && List.member aj rangej


getKey : Model -> Nav.Key
getKey model = model.key

view : Model -> H.Html Msg
view model =
  H.div
    []
    [ H.text model.msg
    , case model.placingError of
      Nothing -> H.div [] []
      Just err -> H.div [ HA.class "error" ] [ H.text <| placingErrorToText err ]
    , H.div [ HA.class "us" ]
            [ boardView
              { canSetHead = model.headShip == Nothing
              , canSetTail = model.tailShip == Nothing
              }
              model.ourBoard
            ]
    , H.div [ HA.class "them" ]
            [ boardView
              {canSetHead = False, canSetTail = False}
              model.theirBoard
            ]
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
    List.map
      (\x -> List.map
        (\y -> toSquare (x, y))
        nums
      )
      alphas

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


boardView : Cans -> Board -> H.Html Msg
boardView cans b =
  H.div [ HA.class "board" ]
    <| List.append (letterView "X" :: List.map numView nums)
    <| List.concatMap (alphaSquareView cans) (List.map2 Tuple.pair alphas b)

letterView : String -> H.Html msg
letterView letter = H.div [ HA.class "letter" ][ H.text letter ]

numView : Int -> H.Html ms
numView idx = H.div [ HA.class "num" ][ H.text <| String.fromInt idx ]

alphaSquareView : Cans -> (String, List Square) -> List (H.Html Msg)
alphaSquareView cans (letter, squares) =
  letterView letter :: List.map (squareView cans) squares

squareView : Cans -> Square -> H.Html Msg
squareView {canSetHead, canSetTail} {pos, usedByBoat} =
  let
      (c, i) = pos
      event =
        case (canSetHead, canSetTail) of
          (True, _) -> [HE.onClick <| SetBoatHead pos]
          (_, True) -> [HE.onClick <| SetBoatTail pos]
          (_, _) -> []
      attrs =
        List.append [ HA.class "square"]
        <| if usedByBoat
           then [HA.class "used-by-boat"]
           else event
  in
    H.div attrs [ H.text <| c ++ String.fromInt i ]

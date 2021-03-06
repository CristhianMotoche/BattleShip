module BattleField.Game exposing (Model, Msg, getKey, init, view, update, subs, posToStr)

import Html as H
import Html.Events as HE
import Html.Attributes as HA

import Process
import Task

import Browser.Navigation as Nav

import List.Extra as LE

import BattleField.Websocket as WS
import BattleField.Route as BR


-- MODEL

type alias Model =
  { key : Nav.Key
  , title : Maybe String
  , msg : Maybe String
  , placingError : Maybe PlacingError
  , ourBoard : Board
  , theirBoard : Board
  , headShip : Maybe Pos
  , tailShip : Maybe Pos
  , ourPhase : Phase
  , theirPhase : Phase
  , turn : Turn
  }

type Turn = Ours | Theirs | None

type PlacingError =
  TooLarge | TooSmall | NotInAxis | AlreadyUsed

type Phase = PlacingShips | Ready | Playing

phaseToText : Phase -> String
phaseToText phase =
  case phase of
    PlacingShips -> "Placing ships..."
    Ready -> "Ready!"
    Playing -> "Playing"

phaseFromString : String -> Maybe Phase
phaseFromString str =
  case str of
    "Ready" -> Just Ready
    "Playing" -> Just Playing
    "PlacingShips" -> Just PlacingShips
    _ -> Nothing

turnFromStr : String -> Maybe Turn
turnFromStr str =
  case str of
    "Ours" -> Just Ours
    "Theirs" -> Just Theirs
    _ -> Nothing

turnToString : Turn -> String
turnToString turn =
  case turn of
    Ours -> "Ours"
    Theirs -> "Theirs"
    None -> "Game hasn't started"

placingErrorToText : PlacingError -> String
placingErrorToText  err =
  case err of
    TooLarge -> "That position is too far"
    TooSmall -> "That position is too close"
    NotInAxis -> "That position is not in the right axis"
    AlreadyUsed -> "Position already used"

type alias Board = List (List Square)

type alias Pos = (String, Int)

posToStr : Pos -> String
posToStr (str, int) = str ++ String.fromInt int

type alias Square =
  { pos : Pos
  , usedByShip : Bool
  }
type alias Cans =
  { canSetTail : Bool
  , canSetHead : Bool
  }

size : Int
size = 10

shipLen : Int
shipLen = 5

alphas = String.split "" "ABCDEFGHIJ"
nums = List.range 1 size

initBoard : Board
initBoard =
  let
      toSquare pos =
        { pos = pos
        , usedByShip = False
        }
  in
    List.map
      (\x -> List.map
        (\y -> toSquare (x, y))
        nums
      )
      alphas


init : Nav.Key -> Int -> (Model, Cmd Msg)
init key sessionId =
  ({ key = key
   , title = Just "Game"
   , msg = Nothing
   , placingError = Nothing
   , ourBoard = initBoard
   , theirBoard = initBoard
   , headShip = Nothing
   , tailShip = Nothing
   , ourPhase = PlacingShips
   , theirPhase = PlacingShips
   , turn = None
   }
  , WS.wsConnect (BR.wsURL <| BR.Session sessionId)
  )

-- SUBS

subs : Model -> Sub Msg
subs _ =
  Sub.batch
    [ WS.wsIn WSIn
    , WS.wsError WSError
    ]

-- MSG

type Msg =
  WSIn String
  | WSOut String
  | WSError String
  | SetShipHead Pos
  | SetShipTail Pos
  | SendAttack Pos
  | Play
  | RedirectError


-- UPDATE

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    WSIn str ->
      case (phaseFromString str, turnFromStr str) of
        (Just phase, _) -> ({model | theirPhase = phase}, Cmd.none)
        (_, Just yourTurn) -> ({model | turn = yourTurn}, Cmd.none)
        _ -> ({model | msg = Just str}, Cmd.none)

    WSOut str -> (model, WS.wsOut str)

    WSError err ->
      let
          foo = Debug.log "WTF?" err
      in
         ({model | msg = Just err}, redirectAfterShowError)

    RedirectError -> (model, Nav.load <| BR.toString BR.Sessions)

    Play -> ({ model | ourPhase = Playing }, WS.wsOut "Playing")

    SetShipHead pos ->
        ({ model |
           ourBoard = setShipHead pos model.ourBoard,
           headShip = Just pos
         }, WS.wsOut "Placing")

    SendAttack pos -> (model, WS.wsOut <| posToStr pos)

    SetShipTail pos ->
      case model.headShip of
        Just headPos ->
          case positionAvailable (headPos, pos) model.ourBoard of
            Just err -> ({ model | placingError = Just err }, Cmd.none)
            Nothing ->
              ({ model |
                 ourBoard = setShipTail (headPos, pos) model.ourBoard
               , tailShip = Just pos
               , placingError = Nothing
               , ourPhase = Ready
               }, WS.wsOut "Ready")
        Nothing ->
              (model, Cmd.none)


redirectAfterShowError : Cmd Msg
redirectAfterShowError =
  Process.sleep 1000
    |> Task.perform (\_ -> RedirectError)


positionAvailable : (Pos, Pos) -> Board -> Maybe PlacingError
positionAvailable (headPos, tailPos) board =
  let
      ((hi, hj), (ti, tj)) = (headPos, tailPos)
      inAxis = hi == ti || hj == tj
      offset = 1
      alphaToInt a = Maybe.withDefault 0 <| LE.elemIndex a alphas
      distance = abs (alphaToInt hi - alphaToInt ti) + abs (hj - tj) + offset
      tooFar = distance > shipLen
      tooClose = distance < shipLen
  in
     case (inAxis, tooFar, tooClose) of
       (True, False, False) -> Nothing
       (True, True, _) -> Just TooLarge
       (True, _, True) -> Just TooSmall
       (False, _, _) -> Just NotInAxis


setShipHead : Pos -> Board -> Board
setShipHead pos board =
  List.indexedMap
    (\_ squareList ->
      List.indexedMap
        (\_ square ->
            if square.pos == pos
            then { square | usedByShip = True }
            else square
        ) squareList
    ) board

setShipTail : (Pos, Pos) -> Board -> Board
setShipTail positions board =
  List.indexedMap
    (\_ squareList ->
      List.indexedMap
        (\_ square ->
            if memberInLine square.pos positions
            then { square | usedByShip = True }
            else square
        ) squareList
    ) board


memberInLine : Pos -> (Pos, Pos) -> Bool
memberInLine (ai, aj) (h, t) =
  let
      (mxi, mxj) = max h t
      (mni, mnj) = min h t
      genRange (minVal, maxVal) list =
        LE.dropWhile (\a -> a /= minVal)
        <| LE.dropWhileRight (\a -> a /= maxVal)
        <| list
      rangei =  genRange (mni, mxi) alphas
      rangej = genRange (mnj, mxj) nums
  in
    List.member ai rangei && List.member aj rangej

getKey : Model -> Nav.Key
getKey model = model.key

-- VIEW

view : Model -> H.Html Msg
view model =
  H.div
    []
    [ H.text <| turnToString model.turn
    , H.div [ HA.class "our-phase" ]
            [ H.strong [][ H.text "Your status:" ]
            , H.text
                <| phaseToText model.ourPhase ++
                   case model.msg of
                     Just str -> "(" ++ str ++ ")"
                     Nothing -> ""
            ]
    , H.div [ HA.class "their-phase" ]
            [ H.strong [][ H.text "Their status:" ]
            , H.text <| phaseToText model.theirPhase
            ]
    , H.div [ HA.class "play-button"]
            [ if model.ourPhase == Ready
              then H.button [ HE.onClick Play ][H.text "Let's play!"]
              else H.div [] []
            ]
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
squareView {canSetHead, canSetTail} {pos, usedByShip} =
  let
      (c, i) = pos
      event =
        case (canSetHead, canSetTail) of
          (True, _) -> [HE.onClick <| SetShipHead pos]
          (_, True) -> [HE.onClick <| SetShipTail pos]
          (_, _) -> []
      attrs =
        List.append [ HA.class "square"]
        <| if usedByShip
           then [HA.class "used-by-ship"]
           else event
  in
    H.div attrs [ H.text <| c ++ String.fromInt i ]

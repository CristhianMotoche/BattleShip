module BattleField.Session exposing (Model, Msg, init, view, getKey, update)


import Result
import Http
import Html as H
import Html.Attributes as HA
import Browser.Navigation as Nav
import Task as T
import Process as P

import Request.Default as R


type alias Session =
  { id : Int
  , name : String
  }


type alias Model =
  { sessions : List Session
  , key : Nav.Key
  , title : Maybe String
  , status : Status
  }

type Status =
  Failure
  | Loading
  | Success (List Session)


type Msg = Loaded (List Session) | Error


init : Nav.Key -> (Model, Cmd Msg)
init key =
  ({
    sessions = []
  , key = key
  , title = Just "Sessions"
  , status = Loading
  }, loadSessions)

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Loaded list ->
      ({ model | sessions = list, status = Success list}, Cmd.none)
    Error ->
      ({ model | status = Failure }, Cmd.none)

loadSessions : Cmd Msg
loadSessions = R.getSessions {
    onSend = handleResp
  }

handleResp : Result Http.Error () -> Msg
handleResp resp =
    case resp of
      Result.Ok a -> Loaded [{ id = 1, name = "LoL" }]
      Result.Err _ -> Error

view : Model -> H.Html Msg
view model =
  case model.status of
    Loading ->
      H.div [ HA.class "loading" ]
            [ H.text "Loading..." ]
    Failure ->
      H.div [ HA.class "Failure" ]
            [ H.text "Something went wrong..." ]
    Success listSessions ->
      H.div [ HA.class "sessions" ]
            [ H.div []
                    (List.map viewSession listSessions)]

viewSession : Session -> H.Html Msg
viewSession session =
  H.div [ HA.class "session" ]
        [ H.text (String.fromInt session.id)
        , H.text session.name
        ]

getKey : Model -> Nav.Key
getKey model = model.key

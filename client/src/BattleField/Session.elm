module BattleField.Session exposing (Model, Status(..), Msg, init, view, viewSessionModel, getKey, update)


import Result
import Data.Session as DS
import Http
import Html as H
import Html.Attributes as HA
import Browser.Navigation as Nav
import Task as T
import Process as P

import Request.Default as R


type alias Session = DS.Session


type alias Model =
  { key : Nav.Key
  , title : Maybe String
  , model : SessionModel
  }


type alias SessionModel =
  { sessions : List Session
  , status : Status
  }

type Status =
  Failure
  | Loading
  | Success (List Session)


type Msg = Loaded (List Session) | Error


init : Nav.Key -> (Model, Cmd Msg)
init key =
  ({ key = key
     , title = Just "Sessions"
     , model = {
       sessions = []
     , status = Loading
     }
  }, loadSessions)

update : Msg -> Model -> (Model, Cmd Msg)
update msg mainModel =
  case msg of
    Loaded list ->
      let {key, model} = mainModel
          newSessionModel = { model | sessions = list, status = Success list}
      in ({mainModel | model = newSessionModel}, Cmd.none)
    Error ->
      let {key, model} = mainModel
          newSessionModel = { model | status = Failure }
      in ({mainModel | model = newSessionModel}, Cmd.none)

loadSessions : Cmd Msg
loadSessions = R.getSessions {
    onSend = handleResp
  }

handleResp : Result Http.Error (List DS.Session) -> Msg
handleResp resp =
    case resp of
      Result.Ok list -> Loaded list
      Result.Err _ -> Error

view : Model -> H.Html Msg
view model = viewSessionModel model.model

viewSessionModel : SessionModel -> H.Html Msg
viewSessionModel model =
  case model.status of
    Loading ->
      H.div [ HA.class "loading" ]
            [ H.text "Loading..." ]
    Failure ->
      H.div [ HA.class "Failure" ]
            [ H.text "Something went wrong..." ]

    Success listSessions ->
      H.div [ HA.class "sessions" ]
            [ H.div [] (List.map viewSession listSessions)]


viewSession : Session -> H.Html Msg
viewSession session =
  H.div [ HA.class "session" ]
        [ H.text (String.fromInt session.id)
        , H.text session.key
        ]

getKey : Model -> Nav.Key
getKey model = model.key

module BattleField.Session exposing (Model, Msg, init, view, getKey, update)


import Html as H
import Html.Attributes as HA
import Browser.Navigation as Nav
import Task as T
import Process as P


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


type Msg = Loaded (List Session)


init : Nav.Key -> (Model, Cmd Msg)
init key =
  ({
    sessions = []
  , key = key
  , title = Just "Sessions"
  , status = Loading
  }, loadSessions)

update : Msg -> Model -> (Model, Cmd Msg)
update (Loaded list) model =
  ({ model | sessions = list, status = Success list}, Cmd.none)

loadSessions : Cmd Msg
loadSessions = T.perform (\_ -> Loaded [{ id = 1, name = "LoL" }]) (P.sleep 2000)

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

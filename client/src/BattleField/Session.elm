module BattleField.Session exposing (Model, Msg, init, view, getKey, update)


import Html as H
import Html.Attributes as HA
import Browser.Navigation as Nav


type alias Session =
  { id : Int
  , name : String
  }


type alias Model =
  { sessions : List Session
  , key : Nav.Key
  , title : Maybe String
  }


type Msg =
  Loading
  | Loaded (List Session)


init : Nav.Key -> Model
init key = {
    sessions = []
  , key = key
  , title = Just "Sessions"
  }

update : Msg -> Model -> (Model, Cmd Msg)
update _ model = (model, Cmd.none)

view : Model -> H.Html Msg
view model =
  H.div [ HA.class "sessions" ]
        [ H.div []
                (List.map viewSession model.sessions)]

viewSession : Session -> H.Html Msg
viewSession session =
  H.div [ HA.class "session" ]
        [ H.text (String.fromInt session.id)
        , H.text session.name
        ]


getKey : Model -> Nav.Key
getKey model = model.key

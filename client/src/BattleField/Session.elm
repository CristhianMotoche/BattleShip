module BattleField.Session exposing (Model, Msg, init, view)


import Html as H
import Html.Attributes as HA


type alias Session =
  { id : Int
  , name : String
  }


type alias Model =
  { sessions : List Session }


type Msg =
  Loading
  | Loaded (List Session)


init : Model
init = {
    sessions = []
  }


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

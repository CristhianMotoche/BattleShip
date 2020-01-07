module BattleField.Index exposing (Model, Msg, init, view, update, getKey)


import Html as H
import Html.Attributes as HA
import Browser.Navigation as Nav

import BattleField.Route as R


type alias Model =
  { title : Maybe String
  , body : ()
  , key : Nav.Key
  }

init : Nav.Key -> Model
init key =
  { title = Nothing
  , body = ()
  , key = key
  }

type alias Msg = ()


update : Msg -> Model -> (Model, Cmd Msg)
update _ model = (model, Cmd.none)


getKey : Model -> Nav.Key
getKey model = model.key


view : Model -> H.Html Msg
view _ =
  H.div
    [ HA.class "index" ]
    [ H.div [ HA.class "index__title" ]
            [ H.h1 []
                   [H.text "BattleField"]],
      H.div [ HA.class "index__play" ]
            [ H.a [ HA.href (R.toString R.Sessions), HA.class "button" ]
                  [ H.text "Play" ]
            , H.a [ HA.href "somewhere", HA.class "button" ]
                  [ H.text "Scores"]]
    ]

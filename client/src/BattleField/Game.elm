module BattleField.Game exposing (Model, Msg, getKey, init, view)

import Html as H

import Browser.Navigation as Nav


type alias Model =
  { key : Nav.Key
  , title : Maybe String
  }

type alias Msg = ()

init : Nav.Key -> Int -> (Model, Cmd Msg)
init key sessionId =
  ({ key = key
   , title = Just "Game"
   }
  , Cmd.none
  )


getKey : Model -> Nav.Key
getKey model = model.key

view : Model -> H.Html Msg
view _ = H.div [] [ H.text "Under construction..." ]

module BattleField.Index exposing (Model, Msg, view, update)


import Html exposing (Html)
import Html as H
import Html.Attributes as HA
import Html.Events as HE


type alias Model = ()

type Msg =
  Play | Scores


update : Msg -> Model -> (Model, Cmd Msg)
update _ model = (model, Cmd.none)


view : Model -> Html Msg
view _ =
  H.div
    []
    [ H.div [] [H.h1 [] [H.text "BattleField"]],
      H.div [] [H.button [HE.onClick Play] [H.text "Play"]],
      H.div [] [H.button [HE.onClick Scores] [H.text "Scores"]]
    ]
    --[ Html.form [HE.onSubmit (WebsocketIn model.input)] -- Short circuit to test without ports

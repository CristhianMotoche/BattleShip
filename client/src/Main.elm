port module Main exposing (main)

import Browser
import Html exposing (Html)
import Html as H
import Html.Attributes as HA
import Html.Events as HE
import Json.Encode as JE

import BattleField.Index.View as IndexView

-- JavaScript usage: app.ports.websocketIn.send(response);
port websocketIn : (String -> msg) -> Sub msg
-- JavaScript usage: app.ports.websocketOut.subscribe(handler);
port websocketOut : String -> Cmd msg

main = Browser.element
    { init = init
    , update = update
    , view = view
    , subscriptions = subscriptions
    }

{- MODEL -}

type alias Model =
    { responses : List String
    , input : String
    }

init : () -> (Model, Cmd Msg)
init _ =
    ( { responses = []
      , input = ""
      }
    , Cmd.none
    )

{- UPDATE -}

type Msg = Change String
    | Submit String
    | WebsocketIn String

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Change input ->
      ( { model | input = input }
      , Cmd.none
      )
    Submit value ->
      ( model
      , websocketOut value
      )
    WebsocketIn value ->
      ( { model | responses = value :: model.responses }
      , Cmd.none
      )

{- SUBSCRIPTIONS -}

subscriptions : Model -> Sub Msg
subscriptions model =
    websocketIn WebsocketIn

{- VIEW -}

li : String -> Html Msg
li string = Html.li [] [Html.text string]

view : Model -> Html Msg
view model =
  H.div
    []
    [ H.div [] [H.h1 [] [H.text "BattleField"]],
      H.div [] [H.button [HE.onClick (Submit "asd")] [H.text "Play"]],
      H.div [] [H.button [HE.onClick (Submit "asd")] [H.text "Scores"]]
    ]
    --[ Html.form [HE.onSubmit (WebsocketIn model.input)] -- Short circuit to test without ports

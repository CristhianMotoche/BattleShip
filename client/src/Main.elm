port module Main exposing (main)

import Browser
import Browser.Navigation as Nav
import Html exposing (Html)
import Html as H
import Html.Attributes as HA
import Html.Events as HE
import Json.Encode as JE
import Url

import BattleField.Index as Index

-- JavaScript usage: app.ports.websocketIn.send(response);
port websocketIn : (String -> msg) -> Sub msg
-- JavaScript usage: app.ports.websocketOut.subscribe(handler);
port websocketOut : String -> Cmd msg


main = Browser.application
    { init = init
    , update = update
    , view = view
    , subscriptions = \_ -> Sub.none
    , onUrlChange = URLChange
    , onUrlRequest = URLRequest
    }

{- MODEL -}

type Model = Index Index.Model

init : () -> Url.Url -> Nav.Key -> (Model, Cmd Msg)
init _ _ _ =
    ( Index ()
    , Cmd.none
    )

{- UPDATE -}

type Msg =
      IndexMsg Index.Msg
    | URLChange Url.Url
    | URLRequest Browser.UrlRequest

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case (msg, model) of
    (IndexMsg msgIndex, Index indexModel) ->
        let
            (newIndexModel, newIndexCmd) = Index.update msgIndex indexModel
        in
           (Index newIndexModel, Cmd.none)
    (URLChange url, _) -> (model, Cmd.none)
    (URLRequest url, _) -> (model, Cmd.none)

{- VIEW -}

view : Model -> Browser.Document Msg
view model =
  case model of
    Index modelIndex ->
      { title = "Title"
      , body = [H.map IndexMsg (Index.view modelIndex)]
      }

port module Main exposing (main)

import Browser
import Browser.Navigation as Nav
import Html as H
import Html.Attributes as HA
import Html.Events as HE
import Json.Encode as JE
import Url

import BattleField.Index as Index
import BattleField.Route exposing (Route)
import BattleField.Route as Route

-- JavaScript usage: app.ports.websocketIn.send(response);
port websocketIn : (String -> msg) -> Sub msg
-- JavaScript usage: app.ports.websocketOut.subscribe(handler);
port websocketOut : String -> Cmd msg


main : Program () Model Msg
main = Browser.application
    { init = init
    , update = update
    , view = view
    , subscriptions = \_ -> Sub.none
    , onUrlChange = URLChange
    , onUrlRequest = URLRequest
    }

{- MODEL -}

type Model =
  Redirect Nav.Key
  | NotFound Nav.Key
  | Index Index.Model

init : () -> Url.Url -> Nav.Key -> (Model, Cmd Msg)
init _ _ key =
    ( Index (Index.init key)
    , Cmd.none
    )

{- UPDATE -}

type Msg =
      IndexMsg Index.Msg
    | URLChange Url.Url
    | URLRequest Browser.UrlRequest
    | None ()

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case (msg, model) of
    (IndexMsg msgIndex, Index indexModel) ->
        let
            (newIndexModel, _) = Index.update msgIndex indexModel
        in
           (Index newIndexModel, Cmd.none)

    (URLChange urlChanged, _) ->
      changeRouteTo (Route.fromUrl urlChanged) model

    (URLRequest urlRequest, _) ->
      case urlRequest of
        Browser.Internal url ->
          ( model, Nav.pushUrl (getKey model) (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )

    (_, _) -> (model, Cmd.none)


changeRouteTo : Maybe Route -> Model -> ( Model, Cmd Msg )
changeRouteTo maybeRoute model =
  case maybeRoute of
    Nothing ->
      (NotFound (getKey model), Cmd.none)
    Just Route.Index ->
      (Index (Index.init (getKey model)), Cmd.none)
    Just Route.Sessions ->
      (model, Cmd.none)


getKey : Model -> Nav.Key
getKey model =
  case model of
    Redirect key -> key
    NotFound key -> key
    Index indexModel -> Index.getKey indexModel


{- VIEW -}

view : Model -> Browser.Document Msg
view model =
  let
      viewPage mkMsg mkView title =
        { title = getTitle title
        , body = [
            H.div [ HA.class "container" ]
                  [ H.map mkMsg mkView ]
          ]
        }
  in
    case model of
      Index modelIndex ->
        viewPage IndexMsg (Index.view modelIndex) modelIndex.title
      Redirect _ -> viewPage None (H.div [][ H.text "Loading.."]) (Just "Redirecting...")
      NotFound _ -> viewPage None (H.div [][ H.text "Not found :("]) (Just "Not Found")

getTitle : Maybe String -> String
getTitle = Maybe.withDefault "BattleField"

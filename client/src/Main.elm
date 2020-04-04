module Main exposing (main)

import Browser
import Browser.Navigation as Nav
import Html as H
import Html.Attributes as HA
import Url

import BattleField.Index as Index
import BattleField.Session as Session
import BattleField.Route as Route

-- JavaScript usage: app.ports.websocketIn.send(response);
-- port websocketIn : (String -> msg) -> Sub msg
-- JavaScript usage: app.ports.websocketOut.subscribe(handler);
-- port websocketOut : String -> Cmd msg


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
  | Sessions Session.Model

init : () -> Url.Url -> Nav.Key -> (Model, Cmd Msg)
init _ url key =
  changeRouteTo (Route.fromUrl url) (Redirect key)

{- UPDATE -}

type Msg =
      IndexMsg Index.Msg
    | SessionMsg Session.Msg
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

    (SessionMsg msgSession, Sessions sessionModel) ->
        let
            (newModel, newCmd) = Session.update msgSession sessionModel
        in
           (Sessions newModel, Cmd.map SessionMsg newCmd)

    (URLChange urlChanged, _) ->
      changeRouteTo (Route.fromUrl urlChanged) model

    (URLRequest urlRequest, _) ->
      case urlRequest of
        Browser.Internal url ->
          ( model, Nav.pushUrl (getKey model) (Url.toString url) )

        Browser.External href ->
          ( model, Nav.load href )

    (_, _) -> (model, Cmd.none)


changeRouteTo : Maybe Route.Route -> Model -> ( Model, Cmd Msg )
changeRouteTo maybeRoute model =
  let key = getKey model
  in
    case maybeRoute of
      Nothing ->
        (NotFound key, Cmd.none)
      Just Route.Index ->
        (Index (Index.init key), Cmd.none)
      Just Route.Sessions ->
        let (x, sessions) = (Session.init key)
        in
          (Sessions x, Cmd.map SessionMsg sessions)
      -- TODO: Implement route
      Just (Route.Session id) ->
        let (x, sessions) = (Session.init key)
        in
          (Sessions x, Cmd.none)


getKey : Model -> Nav.Key
getKey model =
  case model of
    Redirect key -> key
    NotFound key -> key
    Index indexModel -> Index.getKey indexModel
    Sessions sesionModel -> Session.getKey sesionModel


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
      Sessions modelSession ->
        viewPage SessionMsg (Session.view modelSession) modelSession.title
      Redirect _ -> viewPage None (H.div [][ H.text "Loading.."]) (Just "Redirecting...")
      NotFound _ -> viewPage None (H.div [][ H.text "Not found :("]) (Just "Not Found")

getTitle : Maybe String -> String
getTitle = Maybe.withDefault "BattleField"

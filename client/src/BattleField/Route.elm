module BattleField.Route exposing (Route(..), toString, fromUrl, wsURL)

import Url exposing (Url)
import Url.Parser exposing (Parser, map, oneOf, s, parse, top, (</>), int)


type Route
  = Index
  | Sessions
  | Session Int


fromUrl : Url -> Maybe Route
fromUrl = parse routeParser


routeParser : Parser (Route -> a) a
routeParser =
  oneOf
    [ map Index top
    , map Sessions (s "session")
    , map Session (s "session" </> int)
    ]


toString : Route -> String
toString route =
  case route of
    Index -> "/"
    Sessions -> "/session"
    Session id -> "/session/" ++ String.fromInt id


wsURL : Route -> String
wsURL route =
  let
      -- NOTE: This URL is hardcoded for now. Eventually, we should inject it.
      baseURL = "ws://127.0.0.1:5000/ws"
   in
    String.append baseURL <| toString route

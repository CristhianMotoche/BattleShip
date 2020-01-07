module BattleField.Route exposing (Route(..), toString, fromUrl)

import Url exposing (Url)
import Url.Parser exposing (Parser, map, oneOf, s, parse, top)


type Route
  = Index
  | Sessions


fromUrl : Url -> Maybe Route
fromUrl = parse routeParser


routeParser : Parser (Route -> a) a
routeParser =
  oneOf
    [ map Index top
    , map Sessions (s "session")
    ]


toString : Route -> String
toString route =
  case route of
    Index -> "/"
    Sessions -> "/session"

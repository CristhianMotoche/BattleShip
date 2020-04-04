module BattleField.RouteTest exposing (suite)

import BattleField.Route exposing (Route(..), fromUrl, toString)
import Test exposing (Test, describe, fuzz)
import Fuzz exposing (..)
import Expect as E
import Url exposing (Url, Protocol(..))


routeFuzzer : Fuzzer Route
routeFuzzer =
  [ constant Index
  , constant Sessions
  , Fuzz.map Session int
  ]
  |> oneOf


fuzzRoute : Route -> Fuzzer Route
fuzzRoute value =
  case value of
    Index -> constant Index
    Sessions -> constant Sessions
    Session id -> Fuzz.map Session int


formatUrl : String -> Url
formatUrl path =
  { protocol = Http
  , host = "localhost"
  , port_ = Nothing
  , path = path
  , query = Nothing
  , fragment = Nothing
  }


suite : Test
suite =
  describe "Route idempotency"
    [
      fuzz routeFuzzer "(formUrl . toString) r == r" <|
        \route ->
          toString route
            |> formatUrl
            |> fromUrl
            |> E.equal (Just route)
    ]

module BattleField.RouteTest exposing (suite)

import BattleField.Route exposing (Route(..), fromUrl, toString)
import Test exposing (Test, describe, fuzz)
import Fuzz exposing (..)
import Expect as E
import Url exposing (Url, Protocol(..))


routeFuzzer : Fuzzer Route
routeFuzzer =
  oneOf [ constant Index, constant Sessions ]


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

module BattleField.SessionTest exposing (..)

import BattleField.Session exposing (Model, Status(..), viewSessionModel)
import Test exposing (Test, test, describe)
import Test.Html.Query as Query
import Test.Html.Selector as HS

suite : Test
suite =
  describe "Session.view" [testLoading]


testLoading =
  test "Loading" <|
    \() ->
      viewSessionModel ({sessions = [], status = Loading})
      |> Query.fromHtml
      |> Query.has [HS.text "Loading..."]

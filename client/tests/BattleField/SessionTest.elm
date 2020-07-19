module BattleField.SessionTest exposing (..)

import List
import Test exposing (Test, test, describe, fuzz)
import Test.Html.Query as Query
import Test.Html.Selector as HS
import Fuzz exposing (Fuzzer, list)
import Random
import Shrink
import Expect

import Api.Data as DS

import BattleField.Session exposing (SessionModel, Status(..), viewSessionModel)


suite : Test
suite =
  describe
    "Session.view"
    [testLoading, testSuccessEmptyList, testSuccessWithElems]


session : Fuzzer DS.Session
session =
  let generator = Random.map2 DS.Session (Random.int -100 100) (Random.constant "Test")
      shinker { id, key } = Shrink.map DS.Session (Shrink.int id) |> Shrink.andMap (Shrink.string "Test")
    in
       Fuzz.custom generator shinker


testModel : SessionModel
testModel = {
    sessions = []
  , status = Loading
  }


testLoading =
  test "Loading" <|
    \() ->
      viewSessionModel testModel
      |> Query.fromHtml
      |> Query.has [HS.text "Loading..."]


testSuccessEmptyList =
  test "Sucess Empty List" <|
    \() ->
        viewSessionModel ({testModel | status = Success []})
        |> Query.fromHtml
        |> Query.has [HS.text "No sessions to play"]


testSuccessWithElems =
  fuzz (list session) "Sucess" <|
    \sessions ->
        viewSessionModel ({testModel | status = Success sessions})
        |> Query.fromHtml
        |> Query.findAll [ HS.class "session" ]
        |> Query.count (Expect.equal (List.length sessions))

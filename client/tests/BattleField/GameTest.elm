module BattleField.GameTest exposing (..)

import BattleField.Game as BG

import Expect as Exp
import Test exposing (..)


posToStrTest = describe "posToStr"
  [ test "converts position to string" <|
    \_ ->
      BG.posToStr ("A", 1)
      |> Exp.equal "A1"
  ]

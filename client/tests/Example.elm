module Example exposing (..)

import BattleField.Index.View exposing (f)
import Expect exposing (equal)
import Test exposing (..)



suite : Test
suite =
    describe "The String module"
        [ describe "String.reverse" -- Nest as many descriptions as you like.
            [ 
            -- Expect.equal is designed to be used in pipeline style, like this.
            test "reverses a known string" <|
                \_ ->
                    "ABCDEFG"
                        |> f
                        |> equal "ABCDEFG"
            ]
        ]

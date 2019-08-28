module BattleField.Index.View exposing (view)


import Html exposing (Html)
import Html as H
import Html.Attributes as HA
import Html.Events as HE


view : some -> Html some
view some =
  H.div
    []
    [ H.div [] [H.h1 [] [H.text "BattleField"]],
      H.div [] [H.button [HE.onClick some] [H.text "BattleField"]]
    ]

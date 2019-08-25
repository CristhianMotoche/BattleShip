import Browser
import Html exposing (Html, div)
import PortFunnels exposing (State)


-- Main
main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = subscriptions
      }

-- Init
init : () -> (Model, Cmd Msg)
init _ =
    { send = "Hello World!"
    , url = defaultUrl
    , state = PortFunnels.initialState
    , error = Nothing
    } |> withNoCmd


-- Model
type alias Model =
    { send : String
    , url : String
    , state : State
    , error : Maybe String
    }


type Msg = Send


-- Update
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Send -> model |> withNoCmd



-- Subsc
subscriptions : Model -> Sub Msg
subscriptions =
    PortFunnels.subscriptions Process

-- View
view : Model -> Html Msg
view model = div []


--- Websocket
defaultUrl : String
defaultUrl =
  "wss://echo.websocket.org"

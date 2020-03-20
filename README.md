# BattleShip

[![CircleCI](https://circleci.com/gh/CristhianMotoche/BattleShip.svg?style=svg)](https://circleci.com/gh/CristhianMotoche/BattleShip)

## Client
### Requirements
- Elm 0.19.1 (hint: install from [here][elm])
- Node v12.13.1 (hint: use [asdf])
- Docker


### Set up dependencies

Install the dependencies with `npm`:


```
npm install
```

Generate the API client based on the open api definition in the root folder:

```
docker run -v ${PWD}:/tmp \
  openapitools/openapi-generator-cli generate \
  -i /tmp/api.json -g elm -o /tmp/client/generated/
```


### Run parcel

Run `parcel` to load the code with hot reloading:

```
npm run start
```

### Run tests

Run the tests with:

```
npm run test
```

### TODO:
- [ ] Fix Nix dinamyc library not setting the interpreter correctly:
Current workaround:

```
patchelf --set-interpreter \
  /nix/store/681354n3k44r8z90m35hm8945vsp95h1-glibc-2.27/lib/ld-linux-x86-64.so.2 \
  node_modules/elm-test/node_modules/elmi-to-json/unpacked_bin/elmi-to-json
```

## Server
### Requirements

- Python 3.7.5 (tip: install it with [asdf])
- SQLite 3.28.0 (website [here][sqlite])

### Set up

Install dependencies with [poetry]:

```
poetry install
```

### Start up

Run the application with:

```
poetry run app.py
```

### Run tests

Run the tests with:

```
poetry run pytest
```

### Update api.json

Run the following command from the `server` directory:

```
QUART_APP="battlefield:create_app('dev')" poetry run quart openapi > ../api.json
```



[asdf]: https://github.com/asdf-vm/asdf
[poetry]: https://poetry.eustace.io/
[sqlite]: https://sqlite.org/index.html
[elm]: https://guide.elm-lang.org/install/elm.html

# Battlefield
## Client
### Requirements
- Elm 0.19.1 (hint: install from [here][elm])
- Node v12.13.1 (hint: use [asdf])


### Set up dependencies

Install the dependencies with `npm`:


```
npm install
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


[asdf]: https://github.com/asdf-vm/asdf
[poetry]: https://poetry.eustace.io/
[sqlite]: https://sqlite.org/index.html
[elm]: https://guide.elm-lang.org/install/elm.html

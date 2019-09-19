# Battlefield
## Client
### Requirements
- Elm

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
- Python

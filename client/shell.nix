{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    buildInputs = [
      pkgs.elmPackages.elm
      pkgs.nodejs
    ];

    shellHook =
      ''
      export SHELL=$(which zsh)
      zsh
      '';
  }

{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    buildInputs = [
      pkgs.elmPackages.elm
      pkgs.nodejs-10_x
    ];

    shellHook =
      ''
      export SHELL=$(which zsh)
      zsh
      '';
  }

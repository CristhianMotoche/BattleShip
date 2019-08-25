{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    buildInputs = [
      pkgs.elmPackages.elm
    ];

    shellHook =
      ''
      export SHELL=$(which zsh)
      zsh
      '';
  }

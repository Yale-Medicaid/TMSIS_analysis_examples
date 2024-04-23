with import <nixpkgs> {};
  pkgs.mkShell {
    buildInputs = [
      bashInteractive
      python311Packages.mkdocs-material
    ];
    shellHook =
      ''
        mkdocs serve
      '';
  }

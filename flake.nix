{
  description = "HELICS";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    {
      overlay = nixpkgs.lib.composeManyExtensions [
        poetry2nix.overlay
          (final: prev: {
            # we may want this eventually
            # myapp = prev.poetry2nix.mkPoetryApplication {
            #   projectDir = ./.;
            # };

            # seutp a python environment
            myenv = prev.poetry2nix.mkPoetryEnv {
              projectDir = ./.;
            };
          })
        ];
    } // (flake-utils.lib.eachSystem [
    # flake-utils.lib.eachSystem [
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
        "x86_64-linux" ]
    (system: 
      let 
        pybootstrap_pkgs = import nixpkgs {
          inherit system;
        };

        pkgs = import nixpkgs {
          inherit system; 
          overlays = [ self.overlay ];
        };

        packageName = "vip-cosim";

      in {
        packages.myenv = pkgs.myenv;

        devShells.poetry = pybootstrap_pkgs.mkShell {
          buildInputs = with pybootstrap_pkgs; [
            poetry
            python3
          ];
        };

        devShells.default = pkgs.mkShell {

          shellHook = ''
            export PATH=$(realpath ./install/bin):$PATH
            export REPO_ROOT=$(realpath ./.)
          '';

          buildInputs = with pkgs; [
            # C/C++ build utils
            gnumake
            (cmake.override {
              uiToolkits = [ "ncurses" ];
            })
            extra-cmake-modules

            boost
            czmq
            ncurses

            myenv
          ];
        };
      }
    ));
}

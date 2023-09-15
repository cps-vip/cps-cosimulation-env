{
  description = "HELICS";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachSystem [
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
        "x86_64-linux" ]
    (system: 
      let 
        pkgs = import nixpkgs {
          inherit system; 
        };

        packageName = "vip-cosim";

      in {
        devShells.default = pkgs.mkShell {

          shellHook = ''
            source $(realpath ./.)/nix-shell-setup.bash
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

            poetry
            python310
          ];
        };
      }
    );
}

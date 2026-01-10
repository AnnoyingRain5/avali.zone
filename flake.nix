{
  description = "Avali.zone devshell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          (pkgs.python3.withPackages (ppkgs: [
            ppkgs.flask
            ppkgs.flask-dance
            ppkgs.flask-compress
            ppkgs.python-dotenv
            ppkgs.requests
            ppkgs.waitress
          ]))
        ];
        shellHook = "echo \"Want to start a development server? Run 'flask run'\"";
      };
    };
}

{
  description = "Formation LLM — deck Beamer (Makefile + latexmk) et sortie PDF";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAll = f: builtins.listToAttrs (map (s: { name = s; value = f s; }) systems);
      mkShellFor = system:
        let pkgs = import nixpkgs { inherit system; };
        in pkgs.mkShell {
          name = "formation-llm-deck";
          packages = [
            pkgs.texliveFull # latexmk, beamer, tikz, ccicons… (remplace texlive.combined.*, déprécié pour 27.05)
            pkgs.gnumake
            pkgs.git
            pkgs.poppler-utils               # pdftoppm : contrôle visuel des pages
          ];
          shellHook = ''
            echo "make → compile le deck · make view → ouvre le PDF · make clean → range"
          '';
        };
      mkPdfFor = system:
        let pkgs = import nixpkgs { inherit system; };
        in pkgs.stdenv.mkDerivation {
          pname = "formation-llm-deck";
          version = "2026-09";
          src = self;
          nativeBuildInputs = [ pkgs.texliveFull pkgs.gnumake ];
          buildPhase = ''
            runHook preBuild
            export HOME=$TMPDIR
            make
            runHook postBuild
          '';
          installPhase = ''
            runHook preInstall
            install -Dm644 formation_llm.pdf $out/formation_llm.pdf
            runHook postInstall
          '';
        };
    in
    {
      devShells = forAll (system: { default = mkShellFor system; });
      packages = forAll (system: { default = mkPdfFor system; });
    };
}

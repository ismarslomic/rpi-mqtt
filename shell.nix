with (import <nixpkgs> {});

# Build paho-mqtt v2.1.0 as nix package since current nix package release is only v1.6.1
let
  paho = pkgs.python312Packages.buildPythonPackage rec {
    pname = "paho_mqtt";
    version = "2.1.0";

    pyproject = true;

    src = pkgs.python312Packages.fetchPypi {
      inherit pname version;
      hash = "sha256-EtbnUR1BN1VaP26hZ66EavLHNXsQvG+k98OWj8FyODQ=";
    };

    propagatedBuildInputs = with pkgs.python312Packages; [ hatchling ];

    doCheck = false;
  };

  customPython = pkgs.python312.buildEnv.override {
    extraLibs = [ paho ];
  };
in

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.virtualenv
    pkgs.poetry
    pkgs.python312Packages.python-apt
    pkgs.python312Packages.psutil
    pkgs.python312Packages.pyyaml
    pkgs.python312Packages.pydantic
    customPython
  ];
}

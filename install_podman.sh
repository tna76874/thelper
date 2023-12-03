#!/bin/bash

function check_for_podman(){
if ! command -v podman &> /dev/null; then
    sudo apt update > /dev/null 2>&1
    echo "Podman not found. Installing..."
    sudo apt -y install podman
    if [ $? -eq 0 ]; then
        echo "Podman installation successful."
    else
        echo "Error installing Podman. Adding ppa"
        return 1
    fi
else
    echo "Podman is already installed."
fi
}

function add_podman_ppa_and_podman() {
    . /etc/os-release
    echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/ /" | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
    curl -L "https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/xUbuntu_${VERSION_ID}/Release.key" | sudo apt-key add -
    sudo apt update &> /dev/null
    sudo apt -y install podman &> /dev/null
}

function ensure_executeables() {
    executablepathxampp="/usr/local/bin/thelper"
    IMAGE="ghcr.io/tna76874/thelper:latest"

    # Füge die Zeilen zur Datei hinzu
    sudo tee "$executablepathxampp" > /dev/null <<EOF
podman pull $IMAGE > /dev/null 2>&1 || :
podman run -v \$HOME/.config/thelper:/config/.config/thelper -v \$PWD:/work thelper:latest "\$@"
EOF

    sudo chmod +x $executablepathxampp
}

check_for_podman || add_podman_ppa_and_podman && ensure_executeables
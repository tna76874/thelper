#!/bin/bash
podman run --userns=keep-id -v $HOME/.config/thelper:/config/.config/thelper -v $PWD:/work thelper:latest "$@"
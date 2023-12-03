#!/bin/bash
podman run -v $HOME/.config/thelper:/config/.config/thelper -v $PWD:/work thelper:latest "$@"
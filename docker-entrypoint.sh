#!/bin/bash
set -e

extension=${1##*.}
if [[ "$1" == "bash"  ]]; then
    /bin/bash
elif [[ "$extension" == "py"  ]]; then
    /usr/local/bin/python ./"$@"
else
    thelper "$@"
fi

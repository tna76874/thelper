#!/bin/bash
set -e

extension=${1##*.}
if [[ "$1" == "bash"  ]]; then
    exec /bin/bash
elif [[ "$extension" == "py"  ]]; then
    exec /usr/local/bin/python ./"$@"
else
    exec thelper "$@"
fi

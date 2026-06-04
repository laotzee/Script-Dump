#! /bin/bash

qffle_location="$HOME/projects/Qffle"

cd "$qffle_location" || {
    echo "Directory not found"
    exit 1
}

# shellcheck source=/dev/null
source "$qffle_location/.venv/bin/activate" || {
    echo "Failed to activate venv"
    exit 1
}

python cli.py "$1"

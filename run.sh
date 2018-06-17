#!/usr/bin/env bash
ABSPATH=$(cd "$(dirname "$0")" && pwd)

if [ ! -d "$ABSPATH/venv" ]; then
    echo "Virtual env not found under ./venv"
    exit 1
fi

source "$ABSPATH/venv/bin/activate"
"$ABSPATH/explorer.py"

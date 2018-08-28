#!/usr/bin/env bash
ABSPATH=$(cd "$(dirname "$0")" && pwd)

if [ ! -d "$ABSPATH/venv" ]; then
    python3 -m virtualenv "$ABSPATH/venv"
    source "$ABSPATH/venv/bin/activate"
    pip install PyQt5
else
    source "$ABSPATH/venv/bin/activate"
fi

"$ABSPATH/explorer.py"

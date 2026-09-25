#!/bin/bash
# Run on the Pi after requirements.txt changed. ~/sandbox is a mirror
# kept up to date by PyCharm auto-upload (server "pi5"); no git there.

cd ~/sandbox || exit 1
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .    # makes `import sandbox...` work from any directory, as on the Mac

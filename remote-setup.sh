#!/bin/bash
# Run on the Pi after requirements.txt or .python-version changed. ~/sandbox is
# a mirror kept up to date by PyCharm auto-upload / tools/sync_pi.sh; no git there.

cd ~/sandbox || exit 1
[ -d .venv ] || uv venv --seed     # Python version taken from .python-version
uv pip install -r requirements.txt --torch-backend=auto   # CPU torch on the Pi, no CUDA libraries
uv pip install -e .                 # makes `import sandbox...` work from any directory, as on the Mac

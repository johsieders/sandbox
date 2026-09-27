#!/bin/bash
# Run on the Pi after pyproject.toml / uv.lock changed. ~/sandbox is a mirror
# kept up to date by PyCharm auto-upload / tools/sync_pi.sh; no git there.

cd ~/sandbox || exit 1
~/.local/bin/uv sync --locked   # venv + exact versions from uv.lock (CPU torch on the Pi) + editable sandbox

#!/bin/bash
# tools/sync_pi.sh
#
# Mirror the Mac project to the Raspberry Pi (~/sandbox). The Mac is the only
# git repo; the Pi copy is a pure mirror (no git). PyCharm auto-upload (server
# "pi5") misses changes made outside PyCharm and deletions; this fixes that.
#
#   tools/sync_pi.sh        # sync, listing changed/deleted files
#   tools/sync_pi.sh -n     # dry run: only show what would change
#
# After requirements.txt changed, run on the Pi: bash ~/sandbox/remote-setup.sh

PI="jean@192.168.178.115:sandbox/"
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"

rsync -rc --delete --itemize-changes "$@" \
    --exclude=.venv --exclude=.git --exclude=.idea --exclude=__pycache__ \
    --exclude=.pytest_cache --exclude=.DS_Store --exclude=.benchmarks \
    --exclude='*.egg-info' --exclude=.claude \
    "$PROJECT/" "$PI"

#!/bin/bash

cd ~/sandbox || exit 1
git pull
source .venv/bin/activate
pip install -r requirements.txt

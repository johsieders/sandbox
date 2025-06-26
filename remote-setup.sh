#!/bin/bash

cd sandbox || return
git pull
source .venv/bin/activate
pip install -r requirements.txt

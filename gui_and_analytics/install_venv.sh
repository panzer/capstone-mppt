#!/usr/bin/env bash

python -m venv venv

. ./venv/scripts/activate

pip install --upgrade pip

pip install -r requirements.txt
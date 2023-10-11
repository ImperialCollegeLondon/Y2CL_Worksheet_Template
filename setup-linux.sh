#!/bin/bash
python3 -m venv venv
venv/bin/python -m pip install --upgrade pip setuptools wheel
venv/bin/python -m pip install -e .
venv/bin/python .setup-post.py

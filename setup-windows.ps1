python3 -m venv venv
venv/Scripts/python -m pip install --upgrade pip setuptools wheel
venv/Scripts/python -m pip install -e .
venv/Scripts/python .\.setup-post.py

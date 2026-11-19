#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install 'dvc[s3]'
export PYTHONPATH="$PWD/src"
python -m g196_mp020.findings
if [ ! -d .dvc ]; then dvc init; fi
# dvc add removes the tracked working files and leaves .dvc metadata; restore from the original zip if needed.
dvc add data/raw/train.csv data/raw/later.csv data/raw/holdout_features.csv
printf '\nSetup complete. Activate with: source .venv/bin/activate\n'

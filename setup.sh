#!/bin/sh
set -eu

echo "Installing Python dependencies..."
uv sync --no-dev

MODEL_SHA256=5844475f9b551ccda4b68dc2c2deea9cf559405829d1713090064da00505d245

if [ ! -f model/model.bin ] || [ ! -f model/nouns.txt ]; then
  echo "Downloading word embeddings..."
  wget -O model.zip https://dl.furumo.eu/93_filtered_v3.zip
  echo "$MODEL_SHA256  model.zip" | sha256sum -c -
  unzip -o model.zip -d model
  rm model.zip
fi

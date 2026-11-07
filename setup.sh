#!/bin/sh
set -eu

echo "Installing Python dependencies..."
uv sync --no-dev

if [ ! -f model/model.bin ]; then
  echo "Downloading word embeddings..."
  wget -O 93_filtered.zip https://dl.furumo.eu/93_filtered.zip
  unzip -o 93_filtered.zip -d model
  rm 93_filtered.zip
fi

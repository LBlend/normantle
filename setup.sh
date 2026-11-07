#!/bin/sh
set -eu

echo "Installing Python dependencies..."
uv sync --no-dev

MODEL_SHA256=81ea150b00b44b88688a34d822dad84966e6a88c42944f523205fedfeb9c0677

if [ ! -f model/model.bin ]; then
  echo "Downloading word embeddings..."
  wget -O model.zip https://dl.furumo.eu/93_filtered_v2.zip
  echo "$MODEL_SHA256  model.zip" | sha256sum -c -
  unzip -o model.zip -d model
  rm model.zip
fi

#!/bin/sh
set -eu

echo "Installing Python dependencies..."
uv sync --no-dev --group scripts
uv run --no-dev --group scripts python -c "import nltk; nltk.download('stopwords')"

if [ ! -f model/model.txt ]; then
  echo "Downloading word embeddings..."
  wget -O 93.zip https://vectors.nlpl.eu/repository/20/93.zip
  unzip -o 93.zip -d model
  rm 93.zip
fi

echo "Filtering model..."
uv run --no-dev --group scripts python -m scripts.filter_model

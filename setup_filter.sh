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

ORDBANK_SHA256=57d91cb3f17b85befa50a3b56fcaed9800ca665b39486fe97b668add914d5f60

if [ ! -f model/ordbank/lemma.txt ]; then
  echo "Downloading Norsk ordbank..."
  mkdir -p model/ordbank
  wget -O ordbank.tar.gz https://www.nb.no/sbfil/leksikalske_databaser/ordbank/20220201_norsk_ordbank_nob_2005.tar.gz
  echo "$ORDBANK_SHA256  ordbank.tar.gz" | sha256sum -c -
  tar -xzf ordbank.tar.gz -C model/ordbank
  rm ordbank.tar.gz
fi

echo "Filtering model..."
uv run --no-dev --group scripts python -m scripts.filter_model

#!/bin/sh

echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt -U

if [ ! -d 'model' ]; then
    echo "Downloading word embeddings..."
    wget http://vectors.nlpl.eu/repository/20/76.zip
    unzip 76.zip -d model
    rm 76.zip
fi

if [ ! -f 'model/new_model.txt' ]; then
    echo "Filtering model..."
    python3 scripts/filter_model.py
fi

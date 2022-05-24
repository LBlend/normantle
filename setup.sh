#!/bin/sh

echo "Installing Python dependencies..."
python3 setup.py install

if [ ! -d 'model' ]; then
    echo "Downloading word embeddings..."
    wget http://vectors.nlpl.eu/repository/20/76.zip
    unzip 76.zip -d model
fi

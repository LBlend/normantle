#!/bin/sh

echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt -U

if [ ! -d 'model' ]; then
    echo "Downloading word embeddings..."
    wget http://vectors.nlpl.eu/repository/20/93.zip
    unzip 93.zip -d model
    rm 93.zip
fi

python3 -c "import nltk; nltk.download('stopwords')"

echo "Filtering model..."
python3 -m scripts.filter_model

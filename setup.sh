#!/bin/sh

echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt -U

if [ ! -d 'model' ]; then
  wget https://dl.furumo.eu/93_filtered.zip
  unzip 93_filtered.zip -d model
  rm 93_filtered.zip
fi

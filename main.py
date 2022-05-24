from datetime import datetime
from fastapi import FastAPI, HTTPException
import gensim
from models import *
import random


print("Loading model... This might take a while!")
model = gensim.models.KeyedVectors.load_word2vec_format("model/model.bin", binary=True, unicode_errors="replace")
print("Model loaded!")


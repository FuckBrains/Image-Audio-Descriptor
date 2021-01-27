# -*- coding: utf-8 -*-
"""IAD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uQ_v7mVL7JoOO3KB0AANc3_kRklWfZgZ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras
import re
import nltk
from nltk.corpus import stopwords
import string
import json
from time import time
import pickle
from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing import image
from keras.models import Model, load_model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Input, Dense, Dropout, Embedding, LSTM
from keras.layers.merge import add

#from google.colab import drive
#drive.mount('/content/gdrive')

#!ls /content/gdrive/MyDrive

model = load_model("model_9.h5")

model_temp = ResNet50(weights="resnet50_weights_tf_dim_ordering_tf_kernels.h5", input_shape=(224,224,3))

model_resnet = Model(model_temp.input, model_temp.layers[-2].output)

def preprocess_img(img):
    img = image.load_img(img, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    # Normalisation
    img = preprocess_input(img)
    return img

def encode_image(img):
    img = preprocess_img(img)
    feature_vector = model_resnet.predict(img)
    feature_vector = feature_vector.reshape(1,feature_vector.shape[1])
    return feature_vector

#from google.colab import files
#uploaded = files.upload()

#enc = encode_image("img.png")

#enc.shape

#from google.colab import files
#uploaded = files.upload()

with open("word_to_idx.pkl","rb") as w2i:
  word_to_idx = pickle.load(w2i)

#from google.colab import files
#uploaded = files.upload()

with open("idx_to_word(1).pkl", "rb") as i2w:
  idx_to_word = pickle.load(i2w)

def predict_caption(photo):
    max_len = 35
    in_text = "startseq"
    for i in range(max_len):
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence],maxlen=max_len,padding='post')
        
        ypred = model.predict([photo, sequence])
        ypred = ypred.argmax() #WOrd with max prob always - Greedy Sampling
        word = idx_to_word[ypred]
        in_text += (' ' + word)
        
        if word == "endseq":
            break
    
    final_caption = in_text.split()[1:-1]
    final_caption = ' '.join(final_caption)
    return final_caption

#fc = predict_caption(enc)

#fc
#pip install gTTS


from gtts import gTTS
from IPython.display import Audio

def sound_this_image(image):
  enc = encode_image(image)
  caption = predict_caption(enc)
  language = 'en'
  myobj = gTTS(text=caption, lang=language, slow=False)
  myobj.save("output.wav") 
  sound_file = 'output.wav'
  return Audio(sound_file, autoplay=True)

#sound_this_image("img.png")


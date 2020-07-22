import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, GlobalAveragePooling1D, Dense, LSTM, Dropout
from sklearn.model_selection import train_test_split
from keras.models import Sequential
import re
import os

def getData(): 
    data = pd.read_csv('../dataset.csv')
    data = data[:100000]
    #data = data[:10]
    data['text'] = data['text'].apply((lambda x: str(x)))
    tokenizer = Tokenizer(nb_words=5000, lower=True, split=' ')
    tokenizer.fit_on_texts(data['text'].values)

    X_All = tokenizer.texts_to_sequences(data['text'].values)
    X_All = [x[:300] for x in X_All]
    X_All = pad_sequences(X_All)
    Y_All = pd.get_dummies(data['label']).values
    return X_All,Y_All

def getModel():
    embeddingDim = 128
    lstmOutdDim = 200

    model = Sequential()
    model.add(Embedding(5000, embeddingDim,input_length = X_All.shape[1], dropout = 0.2))
    model.add(LSTM(lstmOutdDim, dropout_U = 0.2, dropout_W = 0.2))
    model.add(Dense(2,activation='softmax'))
    model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])

    print(model.summary())
    return model

def saveModel(model):
    model_json = model.to_json()
    with open("LSTMmodel.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("LSTMmodel.h5")
    print("Saved model to disk")

X_All,Y_All=getData()
X_train, X_valid, Y_train, Y_valid = train_test_split(X_All,Y_All, test_size = 0.20, random_state = 36)

model=getModel()

batchSize = 32
model.fit(X_train, Y_train, batch_size =batchSize, nb_epoch = 20,  verbose = 1 ,validation_data=(X_valid, Y_valid)  ) 

saveModel(model)

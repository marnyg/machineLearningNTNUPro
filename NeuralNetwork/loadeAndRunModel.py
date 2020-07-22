from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.optimizers import Adam
import numpy
import os

from dataFormatter import DataFormatter

DataFormatr=DataFormatter()
#Train_X, Test_X, Train_Y, Test_Y = DataFormatr.getDataAs2DMatrix(10000)


# load json and create model
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
print("Loaded model from disk")

adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

loaded_model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])

#score = loaded_model.evaluate(Test_X, Test_Y, verbose=0)
#print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


while True:
  name = input("Enter text: ")
  print(name)
  prediciton=loaded_model.predict(DataFormatr.getSingleSentenseAs2dMatrix(name))
  print('good: ',prediciton[0][0]," bad: ",prediciton[0][1])

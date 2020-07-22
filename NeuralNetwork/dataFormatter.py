from embedding import wordEmbedding
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection
import pandas as pd

class DataFormatter:
  def __init__(self):
    self.dataset = pd.read_csv(r"../dataset.csv")
    self.wordEmb=wordEmbedding()
    self.data=[]

  def getSentensesAs2dMatrixFromDataset(self,numberOfDatapoints):
    wordDimention=50
    sentensLength=300
    sentenses=np.zeros([numberOfDatapoints,sentensLength,wordDimention,1])
    for i in range(numberOfDatapoints):
      for j, word in enumerate( self.dataset["text"][i].split()):
        if j==sentensLength:
          break
        sentenses[i,j]=self.wordEmb.getEmbedding(word.lower()).asnumpy()
    return sentenses.reshape(numberOfDatapoints,sentensLength,wordDimention,1)

  def getSingleSentenseAs2dMatrix(self,sentens):
    matrix=np.zeros([300,50,1])
    for i, word in enumerate(sentens.split()):
      if i==300: 
        break
      matrix[i]=self.wordEmb.getEmbedding(word.lower()).asnumpy()
    return matrix.reshape(1,300,50,1)
  
  def prosessData(self,numberOfDatapoints):
    import os
    file='cache'+str(numberOfDatapoints)+'.npy'
    if os.path.isfile(file):
      self.data=np.load(file)
    else:
      self.data=self.getSentensesAs2dMatrixFromDataset(numberOfDatapoints)
      np.save(file, self.data)

  def getDataAs2DMatrix(self, numberOfDatapoints):
    self.prosessData(numberOfDatapoints)
    self.splitTrainTest(numberOfDatapoints)
    return self.Train_X,self.Test_X,self.Train_Y,self.Test_Y
  
  def splitTrainTest(self,numberOfDatapoints):
    labels= [(0 if x=='g' else 1) for x in self.dataset['label']]
    self.Train_X, self.Test_X, Train_Y, Test_Y = model_selection.train_test_split(self.data,labels[0:numberOfDatapoints],test_size=0.3)
    self.Train_Y=to_categorical(Train_Y)
    self.Test_Y=to_categorical(Test_Y)

  def LSTMgetSentensesAs2dMatrixFromDataset(self,numberOfDatapoints):
      #WHYYYYY
    wordDimention=50
    sentensLength=300
    sentenses=np.zeros([numberOfDatapoints,sentensLength,wordDimention])
    for i in range(numberOfDatapoints):
      for j, word in enumerate( self.dataset["text"][i].split()):
        if j==sentensLength:
          break
        sentenses[i,j]=self.wordEmb.getEmbedding(word.lower()).reshape(50).asnumpy()
    return sentenses

  def LSTMprosessData(self,numberOfDatapoints):
    import os
    file='LSTMcache'+str(numberOfDatapoints)+'.npy'
    if os.path.isfile(file):
      self.data=np.load(file)
    else:
      self.data=self.LSTMgetSentensesAs2dMatrixFromDataset(numberOfDatapoints)
      np.save(file, self.data)

  def LSTMgetDataAs2DMatrix(self, numberOfDatapoints):
    self.LSTMprosessData(numberOfDatapoints)
    self.splitTrainTest(numberOfDatapoints)
    return self.Train_X,self.Test_X,self.Train_Y,self.Test_Y

  def getLabels(self, first_n_examples):
    # Returns the labels of the first n examples from the dataset, as numpy array of one-hots (dummies). E.g.: row with 'label' = 'g' becomes np.array = [0, 1]
    s = self.dataset[:first_n_examples]['label']
    labels = pd.get_dummies(s)
    return labels.values



#test=DataFormatter()
#a,b,c,d=test.getDataAs2DMatrix(1000)
#print(a.shape,b.shape,c.shape,d.shape)


#sentenses= getSentensesAs2dMatrixFromDataset(numberOfDatapoints)





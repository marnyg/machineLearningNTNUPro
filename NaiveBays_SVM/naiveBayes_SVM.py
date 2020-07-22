import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

np.random.seed(500)

def readData(path,limit):
    Corpus = pd.read_csv(path)
    print(len(Corpus))
    Corpus=Corpus[0:limit]
    Corpus['text'] = [str(entry).lower() for entry in Corpus['text']]
    Corpus['text']= [word_tokenize(entry) for entry in Corpus['text']]
    return Corpus

def crateTagMap():
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    return tag_map

def tokenizeWords(Corpus):
    tag_map=crateTagMap()

    for index,entry in enumerate(Corpus['text']):
        Final_words = []
        word_Lemmatized = WordNetLemmatizer()
        for word, tag in pos_tag(entry):
            if word not in stopwords.words('english') and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                Final_words.append(word_Final)
        Corpus.loc[index,'text_final'] = str(Final_words)


def getData():
    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['text_final'],Corpus['label'],test_size=0.3)

    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Train_Y)
    Test_Y = Encoder.fit_transform(Test_Y)

    # Vectoriser ord
    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(Corpus['text_final'])

    Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    Test_X_Tfidf = Tfidf_vect.transform(Test_X)
    return Train_Y,Test_Y,Train_X_Tfidf,Test_X_Tfidf

def doNaivebayes():
    Naive = naive_bayes.MultinomialNB()
    Naive.fit(Train_X_Tfidf,Train_Y)

    predictions_NB = Naive.predict(Test_X_Tfidf)

    print("Naive Bayes Accuracy Score -> ",accuracy_score(predictions_NB, Test_Y)*100)

def doSVM():
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    SVM.fit(Train_X_Tfidf,Train_Y)

    predictions_SVM = SVM.predict(Test_X_Tfidf)

    print("SVM Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)

def checkCache(numberOfDatapoints):
    import os
    Corpus=None
    file='cache'+str(numberOfDatapoints)+'.npy'
    if os.path.isfile(file):
      print('iz htere')
      Corpus = pd.read_csv(file)
    else:
      print("not there")
      Corpus=readData("../dataset.csv",numberOfDatapoints)
      tokenizeWords(Corpus)
      Corpus.to_csv(file,index=False)
    return Corpus

Corpus=checkCache(10000)
Train_Y,Test_Y,Train_X_Tfidf,Test_X_Tfidf=getData()
doNaivebayes()
doSVM()




import pandas as pd
import numpy as np

# Define the classes
HATE_SPEECH = 0
OFFENSIVE_LANGUAGE = 1
NEITHER = 2

# Read the raw csv file
columns = ['count', 'hate_speech' , 'offensive_language' , 'neither' , 'class', 'tweet']
df = pd.read_csv('../Dataset/Hate Speech Dataset/data/labeled_data.csv', header=0, names=columns)

# Sepparate the tweets by classes into sepparate pandas DataFrames
hate_speech = df.loc[df['class'] == HATE_SPEECH] 
offensive_language = df.loc[df['class'] == OFFENSIVE_LANGUAGE]
neither = df.loc[df['class'] == NEITHER] 

print('Total number of tweets:', df.shape[0])
print('Number of hate speech tweets:', hate_speech.shape[0])
print('Number of offensive language speech tweets:', offensive_language.shape[0])
print('Number of neither tweets:', neither.shape[0])

import re

cleaned_labels = ['g', 'b']
GOOD = cleaned_labels[0]
BAD = cleaned_labels[1]

def clean(dataframe, label): # Removes all substrings that are not relevant. E.g.: usertags, emojis, etc. Only words and simple signs (?, !, ., etc.) will be returned, all marked with label
    cleaned = []
    for i in range(dataframe.shape[0]):
        tweet = dataframe['tweet'].iloc[i]
        no_quotes_reg = r'"+|:+'
        no_quotes = re.sub(no_quotes_reg, '', tweet)
        no_emojis = re.sub(r'\&#[0-9]*;', '', no_quotes) # Remove all occurences of the string &#NUMBER; (think this is some emoji)
        user_tag_reg = r'@\w+\s+' # Maches user-tags|@.*\s+
        no_tags = re.sub(user_tag_reg, '', no_emojis) # Remove user-tags (reference to another user. E.g. @TheRealLeonardoDaVinci)
        no_links_reg = r'http.+//.+\s|http.+//.+'
        no_links = re.sub(no_links_reg, '', no_tags)
        cleaned.append([no_links, label])
    output = pd.DataFrame(data=cleaned, columns=['tweet', 'label'])
    return output

cleaned_bad_1 = clean(hate_speech, BAD)
cleaned_bad_2 = clean(offensive_language, BAD)
cleaned_bad = cleaned_bad_1.append(cleaned_bad_2, ignore_index=True)
cleaned_good = clean(neither, GOOD)
cleaned = cleaned_bad.append(cleaned_good, ignore_index=True)

cleaned_bad.columns = ['text', 'label']
cleaned_good.columns = ['text', 'label']
cleaned.columns = ['text', 'label']

cleaned_good.to_csv('hate_speech_good.csv', index=False)
cleaned_bad.to_csv('hate_speech_bad.csv', index=False)
cleaned.to_csv('../Dataset/Hate Speech Dataset/hate_speech.csv', index=False)
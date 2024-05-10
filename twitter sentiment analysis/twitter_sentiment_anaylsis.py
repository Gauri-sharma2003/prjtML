# -*- coding: utf-8 -*-
"""twitter_sentiment_anaylsis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QrfEuUMEWtQCTrZYkOEYabNjTvhqMFcJ
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

arr1=np.array([])
k1=0;
k2=0;
k3=0;
path="/content/twitter.csv"
myfile=pd.read_csv(path)
for i in range(len(myfile)):
# precprcess tweet
  tweet=myfile.iloc[i, 0]
  tweet_words = []

  for word in tweet.split(' '):
      if word.startswith('@') and len(word) > 1:
          word = '@user'

      elif word.startswith('http'):
          word = "http"
      tweet_words.append(word)

  tweet_proc = " ".join(tweet_words)

  # load model and tokenizer
  roberta = "cardiffnlp/twitter-roberta-base-sentiment"

  model = AutoModelForSequenceClassification.from_pretrained(roberta)
  tokenizer = AutoTokenizer.from_pretrained(roberta)

  labels = ['Negative', 'Neutral', 'Positive']

  # sentiment analysis
  encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
  # output = model(encoded_tweet['input_ids'], encoded_tweet['attention_mask'])
  output = model(**encoded_tweet)

  scores = output[0][0].detach().numpy()
  scores = softmax(scores)
  a=np.array([scores[0],scores[1],scores[2]])
  d=a.argmax()
  if(labels[d]=='Negative'):
    k1=k1+1
  elif(labels[d]=='Positive'):
    k2=k2+1
  else:
    k3=k3+1

y = np.array([k1,k3,k2])
mylabels = ["Negative", "Neutral", "Positive"]
plt.pie(y, labels = mylabels, startangle = 90, autopct='%1.0f%%')
plt.show()
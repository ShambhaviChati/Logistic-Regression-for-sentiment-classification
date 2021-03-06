# -*- coding: utf-8 -*-
"""IDS566 - HW2 - claudia.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eIJi4Mmx9WkvhWr4AIlFGdqzVnWrVtEW
"""

#Call Package 
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pandas as pd
import nltk, string, numpy
from sklearn.metrics import jaccard_similarity_score
ps = PorterStemmer()
import re
from scipy.optimize import fmin_tnc
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import numpy.linalg as LA

#Read train data
import pandas as pd
file12 = pd.read_csv('train_90.txt',sep=',',header = 0)
file11 = pd.read_csv('test_10.txt',sep=',',header = 0)
file12.head()

#Train Data Size & Cols
print('Dataset size:',file12.shape)
print('Columns are:',file12.columns)

#Train Text to Remove Punctuation
def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

file12['Sentiment_punct'] = file12['SentimentText'].apply(lambda x: remove_punct(x))
file11['Sentiment_punct'] = file11['SentimentText'].apply(lambda x: remove_punct(x))
file12.head(10)

#Train Remove Punctiation to Tokenization
def tokenization(text):
    text = re.split('\W+', text)
    return text

file12['Sentiment_tokenized'] = file12['Sentiment_punct'].apply(lambda x:tokenization(x.lower()))
file11['Sentiment_tokenized'] = file11['Sentiment_punct'].apply(lambda x:tokenization(x.lower()))
file12.head()

#Train Tokenize to NonStop
stopword = nltk.corpus.stopwords.words('english')
def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text
    
file12['Sentiment_nonstop'] = file12['Sentiment_tokenized'].apply(lambda x: remove_stopwords(x))
file11['Sentiment_nonstop'] = file11['Sentiment_tokenized'].apply(lambda x: remove_stopwords(x))
file12.head(10)

#Data frame for Train & test
df_train = pd.DataFrame(file12, columns = ['Sentiment', 'Sentiment_nonstop'])
df_test = pd.DataFrame(file11, columns = ['Sentiment', 'Sentiment_nonstop'])

print(df_train.head())

df_test["Sentiment_nonstop"]= df_test["Sentiment_nonstop"].str.join(" ")
df_train["Sentiment_nonstop"]= df_train["Sentiment_nonstop"].str.join(" ")

df_test['Sentiment_nonstop'].head()

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_features=200, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
# TF-IDF feature matrix
tfidf = tfidf_vectorizer.fit_transform(df_train['Sentiment_nonstop']).toarray()
tfidf_test=tfidf_vectorizer.fit_transform(df_test['Sentiment_nonstop']).toarray()

type(tfidf)

print('Dataset size:',tfidf.shape)

X=tfidf
X_test=tfidf_test
print(X.shape)
type(X)

df_train['Sentiment']=df_train['Sentiment'].astype(int)
df_test['Sentiment']=df_test['Sentiment'].astype(int)

Y=df_train['Sentiment']
Y_test=df_test['Sentiment']

theta = np.zeros((X.shape[1], 1))

def func1(x):
    a=1/(1+np.exp-x)
    return a

def func2(theta,x):
    b=np.dot(x,theta)
    return b

def prob(theta,x):
    c=sigmoid(net_input(theta,x))
    return c

def cost(theta,x,y):
    m=x.shape[0]
    tcost=-(1/m)*np.sum(y*np.log(prob(theta,x))+(1-y)*np.log(1-prob(theta,x)))
    return tcost

def gradient(theta,x,y):
    m=x.shape[0]
    grad=(1/m)*np.dot(x.T, func1(func2(theta,x))-y)
    return grad

def fit_func(x, y, theta):
    weights=fmin_tnc(func=cost,x0=theta,fprime=gradient,args=(x,y.values.flatten()))
    return weights[0]
parameters= fit(X,Y,theta)

def pred(x):
    theta = parameters[:,np.newaxis]
    return prob(theta,x)
def acc(x, actual_classes,probab_threshold=0.5):
    pred_classes= (pred(x)>=probab_threshold).astype(int)
    pred_classes=pred_classes.flatten()
    acc=np.mean(pred_classes==actual_classes)
    return acc
acc(X,Y.values.flatten())

from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
seed = 7
kfold=KFold(n_splits=10, random_state=seed, shuffle= True)
model=LogisticRegression()
results=cross_val_score(model,tfidf,df_train['Sentiment'],cv=kfold)
print("Accuracy: %.3f%% (%.3f%%)" % (results.mean()*100.0,results.std()*100.0))

def acc_test(x,actual_classes,probab_threshold=0.5):
    pred_classes=(pred(x)>=probab_threshold).astype(int)
    pred_classes=pred_classes.flatten()
    return confusion_matrix(actual_classes,pred_classes)

confusion=acc_test(X_test,Y_test.values.flatten())

precision=confusion[0][0]/(confusion[0][0]+confusion[0][1])
print(precision)
recall=confusion[0][0]/(confusion[0][0]+confusion[1][0])
print(recall)




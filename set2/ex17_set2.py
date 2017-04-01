# -*- coding: utf-8 -*-
#
#Develop a text classifier for a kind of texts of your choice (e.g., e-mail messages, tweets,
#customer reviews) and at least two classes (e.g., spam/ham, positive/negative/neutral).
#You should write your own code to convert each (training, validation, or test) text to a feature
#vector. You may use Boolean, TF, or TF-IDF features corresponding to words or n-grams, to
#which you can also add other features (e.g., length of the text).3 You may apply any feature
#selection (or dimensionality reduction) method you consider appropriate. You may also want
#to try using centroids of pre-trained word embeddings (slide 35). You can write your own
#code to perform feature selection (or dimensionality reduction) and to train the classifier (e.g.,
#using SGD and the tricks of slides 58 and 59, in the case of logistic regression), or you can
#use existing implementations.5 You should experiment with at least logistic regression, and
#optionally other learning algorithms (e.g., Naive Bayes, k-NN, SVM). Draw learning curves
#(slides 64, 67) with appropriate measures (e.g., accuracy, F1) and precision-recall curves
#(slide 23). Include experimental results of appropriate baselines (e.g., majority classifiers).
#Make sure that you use separate training and test data. Tune the feature set and hyperparameters
#(e.g., regularization weight λ) on a held-out part of the training data or using a
#cross-validation (slide 25) on the training data. Document clearly in a short report (max. 10
#pages) how your system works and its experimental results.

import codecs
import os
import nltk

def tokenizer(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    return tokens

def count_occur(words): #find the occurences of each token
    counter={}
    for i in set(words):
        counter[i] = 0
    for token in words:
        counter[token]+=1
    return counter


def create_voc(email_files,language):
    stopwords = nltk.corpus.stopwords.words(language)
    f_tokens = []
    symbols = ["{",'}',"@","(",")","[","]",".",":",";","+","-","*","/","&","|","<",">","=","~",'"',","]
    tokens = []
    for i in email_files:
        mid = tokenizer(i)
        mid = [l for l in mid if not str(l).isdigit()]
        tokens.extend([k for k in mid if k not in symbols and k not in stopwords])
    counter = count_occur(tokens)
    for token in counter.keys():
        if counter[token]>=20: # we let ! because it is very common in spam files!
            f_tokens.append(token)
    return f_tokens,counter

def sieve(text,true_vocabulary):
    tokens = tokenizer(text)
    sent_back = []
    for i in tokens:
        if i in true_vocabulary:
            sent_back.append(i)
    return sent_back

def freq_vector(email,vocabulary):
    pass    

stopwords = nltk.corpus.stopwords.words('english')
ham_path = os.path.join(os.getcwd(),"enron1","ham" )
spam_path= os.path.join(os.getcwd(),"enron1","spam" )

ham_files = []
spam_files = []

for root,directories,files in  os.walk(ham_path):
    for f in files:
        f1 = codecs.open(ham_path+os.sep+f,"r","utf-8",errors='ignore')
        ham_files.append(f1.read())
        f1.close()
        
for root,directories,files in  os.walk(spam_path):
    for f in files:
        f2 = codecs.open(spam_path+os.sep+f,"r","utf-8",errors='ignore')
        spam_files.append(f2.read())
        f2.close()

filtered_tokens,occurences= create_voc(ham_files+spam_files,'english')
filtered_tokens = set(filtered_tokens)
#doing the preprocessesing for the feature selection
all_labeled = [ (sieve(i,filtered_tokens),'ham') for i in ham_files]
all_labeled.extend([ (sieve(i,filtered_tokens),'spam') for i in spam_files])

from __future__ import print_function
import numpy as np
import json
from scipy.sparse import csc_matrix
from sklearn import metrics
import sys, os
import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import json
import operator
from pprint import pprint
import gensim
import re
import codecs
from tweepy import OAuthHandler
import tweepy
from samplegeo import findCountry
import matplotlib.pyplot as plt

def text_clean(text):

    remove_space = '\s+'
    find_url = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
        '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    find_mention = '@[\w\-]+'
    process_text = re.sub(remove_space, ' ', text)
    process_text = re.sub(find_url, '', process_text)
    process_text = re.sub(find_mention, '', process_text)
    process_text = process_text.encode('ascii','ignore')
    return process_text

con_key = 'PG2atN7eFZIfjqPugmrQ0DTHN'
con_secret = 'BcKjeAsjePUjw5SqOj7DqQy7QgTvNo6fbNXoT6PHoV68CwqWSX'
acc_token = '93137600-fD6r6VCcwx2f4ahKrqTlImxhFicNYcpy17HkL8Ne4'
acc_token_secret = 'lYUwaYoI6j5nHk7pijChJUxzDuY99osg64rs9vjhOejWU'

try:
            auth = OAuthHandler(con_key, con_secret)
            auth.set_access_token(acc_token, acc_token_secret)
            api = tweepy.API(auth)
            
except:
            
            print("Error: Twitter Not Connected")


def getTweetLocation(searchTxt):
        query = "#"+searchTxt
        count = 40
        tweets = []
        clean_tweets=[]
        try:
                    fetched_tweets = api.search(q = query, count = count)
                    cnt=0;
         
                    for tweet in fetched_tweets:
                        parsed_tweet = {}
                        
                        parsed_tweet['tweet']=tweet._json
                        parsed_tweet['country']=findCountry((tweet._json))
                        clean_tweets.append(parsed_tweet)
                        print("\r Processing...",cnt,"\r")
                        cnt=cnt+1
       
                    
                    df = pd.DataFrame(clean_tweets)
                    df.to_csv("clean_tweets.csv")

                    
                    # a simple line plot
                    df=pd.read_csv("clean_tweets.csv")
                    df.groupby('country')['tweet'].nunique().plot(kind='bar')
                    plt.savefig("tweet.png")
#                   plt.show()

                    
            
         
        except tweepy.TweepError as e:
               print("Error : " + str(e))

        print ("*********************************")
        print ("Total tweets read from twitter server ")
        print (len(tweets))

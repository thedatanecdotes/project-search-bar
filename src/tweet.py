# for tweet API
import pandas as pd
import time
import numpy as np
import os
import re
import contractions
import nltk
import tweepy 
import seaborn as sns
from datetime import date
from nltk.stem.wordnet import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment=SentimentIntensityAnalyzer()
words=set(nltk.corpus.words.words())
def get_api():
    consumer_key = 'K8hMFAwqdNtVdoOfXs7M7PuX2'
    consumer_secret = '9NDahtLV8Yr53wLsbrXsrXO6Ld8XzvvvdigAUauEwrXSUABSQf'
    access_key= '1342222528966619136-XMYn5J5gbkmhsKarXvQnCHLftgESIY'
    access_secret = 'wE5YdJVoCV8Qi75qgxDOJb6Ww9XhQXY7bEUxuCXiQ0LZz'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    return api
def clean_txt(input_txt, pattern):
    #removing hashtags,emojis,stopwords
    input_txt=re.sub(r'#[\w]*','',input_txt)
    input_txt=input_txt.encode("ascii","ignore")
    input_txt=input_txt.decode()
    
    ##removing @user
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
   
    #removing stopwords    
    input_txt = ' '.join([i for i in input_txt.split() if not i in words])
    #contractions
    input_txt=contractions.fix(input_txt)
    #removing punctuation,numbers and whitespace   
    res=re.sub(r'[^\w\s]', '', input_txt.lower())
    res=re.sub('\s+',' ',res)
    ##removing links
    res=re.sub(r'https[\w]*', '', res, flags=re.MULTILINE)
    #removing acronyms
    res=''.join(i for i in res if not i.isdigit())
    res=' '.join([i for i in res.split() if len(i)>2])
    lem = WordNetLemmatizer()
    res = lem.lemmatize(res)
    
    return res
def get_sentiment(data):
    ss=[]
    for _,row in data.iterrows():
        sent_dict=sentiment.polarity_scores(row['Clean Tweets'])
        if(sent_dict['compound']>=0.05):
            ss.append("POSITIVE")
        elif(sent_dict['compound']<=-0.05):
            ss.append("NEGATIVE")
        else:
            ss.append("NEUTRAL")
    return ss
def get_data(keyword,api):
    data={"Date":[],"Tweet":[],"Tweet Source":[],"Retweets":[],"Likes":[],"Location":[]}
    for tweet in tweepy.Cursor(api.search,q=keyword+"-filter:retweets",count=1000,lang="en",until=date.today(),tweet_mode="extended").items():
           if(len(data['Tweet'])<1000):
                #st.write("Tweets extracted",len(data['Tweet']))
                data['Date'].append(tweet.created_at)
                data['Tweet'].append(tweet.full_text)
                data['Location'].append(tweet.user.location)
                data['Tweet Source'].append(tweet.source)
                data['Retweets'].append(tweet.retweet_count)
                data['Likes'].append(tweet.favorite_count)
           else:
               break
    data=pd.DataFrame.from_dict(data,orient="index").transpose()
    data['Clean Tweets']=[clean_txt(row['Tweet'],"@[\w]*") for _,row in data.iterrows()]
    data['SS']=get_sentiment(data)
    data['Date']=pd.to_datetime(data['Date'])
    return data

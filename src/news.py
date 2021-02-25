from newsapi import NewsApiClient
import streamlit as st
import os
from newspaper import fulltext
import requests
from summary import generate_summary
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

newsapi = NewsApiClient(api_key='c72b4aa180274136b01201d248dac4aa')
analyzer = SentimentIntensityAnalyzer()

def process_news(article_url,min_sentence = 5):
    try:
        article = fulltext(requests.get(article_url).text)
        article = generate_summary(article,min_sentence)
        article = re.sub(r"\<[^ ]*\>", "", article)
        return article

    except Exception as e: 
        print(e)
        return -1

def news_sentiments(keyword,num=5,min_sentence = 5):
    all_articles = newsapi.get_top_headlines(q=keyword,language='en',country="in")
    urls=[i['url'] for i in all_articles['articles']][:num]
    news = [process_news(i,min_sentence) for i in urls]
    while(news.count(-1)>0):
        urls.remove(urls[news.index(-1)])
        news.remove(-1)
    sentiments = [analyzer.polarity_scores(i)['compound'] for i in news]
    for i in range(len(sentiments)):
        c = sentiments[i]
        if c>=0.05:
            sentiments[i] = "Positive"
        elif c<=-0.05:
            sentiments[i] = "Negative"
        else:
            sentiments[i] = "Neutral"

    result = {}
    for i in range(len(news)):
        result[i] = {
            'News Summary': news[i],
            'Source': urls[i],
            'Sentiment': sentiments[i]
            }
    
    return result



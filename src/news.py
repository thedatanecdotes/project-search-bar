from GoogleNews import GoogleNews
from newsapi import NewsApiClient
import os
from newspaper import fulltext
import requests
from summary import generate_summary
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

newsapi = NewsApiClient(api_key=os.environ.get('news_api'))
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

def news_sentiments(topic_name,num=10,min_sentence = 5):

    print("Fetching News...")
    all_articles = newsapi.get_everything(q=topic_name,language='en',sort_by='relevancy')
    if(all_articles['totalResults']==0):
        return "Sorry! No articles related to the keyword found."

    print("Summarising News...")
    news = [process_news(i['url'],min_sentence) for i in all_articles['articles']][:num]
    print(len(news))
    while(news!=None and news.count(-1)>0):
        urls = urls.remove(urls[news.index(-1)])
        news = news.remove(-1)
    
    print("Finding Sentiment...")
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
            'Source': all_articles['articles'][i]['url'],
            'Sentiment': sentiments[i]
            }
    
    return result
    
res=news_sentiments('farmbills',5)


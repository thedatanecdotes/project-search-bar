from GoogleNews import GoogleNews
from newspaper import fulltext
import requests
from summary import generate_summary
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import re

googlenews = GoogleNews()
googlenews.set_lang('en')
googlenews.set_period('5d')
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
    googlenews.get_news(topic_name)
    urls = googlenews.get_links()[:num]
    googlenews.clear()

    print("Summarising News...")
    news = [process_news("http://"+url,min_sentence) for url in urls]
    
    while(news!=None and news.count(-1)>0):
        urls = urls.remove(urls[news.index(-1)])
        news = news.remove(-1)
    
    if news == None:
        return "Error"

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
    for i in range(num):
        result[i] = {
            'news': news[i],
            'author': "http://"+urls[i],
            'sentiment': sentiments[i]
            }
    
    return result
    
print(news_sentiments("Farmer's Protest",3))

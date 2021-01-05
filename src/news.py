from GoogleNews import GoogleNews
from newspaper import fulltext
import requests
from transformers import *
import re

googlenews = GoogleNews()
googlenews.set_lang('en')
googlenews.set_period('5d')
summary = pipeline("summarization")
sentiment = pipeline('sentiment-analysis')

def process_news(article_url,min_length = 60):
    try:
        article = fulltext(requests.get(article_url).text)
        article = summary(article,min_length=min_length)[0]['summary_text']
        article = re.sub(r"\<[^ ]*\>", "", article)
        return article
    except Exception as e: 
        print(e)
        return -1

def news_sentiments(topic_name,num=10,min_length = 60):

    googlenews.get_news(topic_name)
    urls = googlenews.get_links()[:num]
    googlenews.clear()

    news = [process_news("http://"+url,min_length) for url in urls]
    
    while(news!=None and news.count(-1)>0):
        urls = urls.remove(urls[news.index(-1)])
        news = news.remove(-1)
    
    if news == None:
        return "Error"

    sentiments = [sent['label'] for sent in sentiment(news)]
    

    result = {}
    for i in range(num):
        result[i] = {
            'news': news[i],
            'author': urls[i],
            'sentiment': sentiments[i]
            }
    
    return result
    
# print(news_sentiments("Farmer's Protest",3))

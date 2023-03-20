import requests
from newsapi import NewsApiClient

# Replace 'YOUR_NEWS_API_KEY' with your actual News API key
newsapi = NewsApiClient(api_key='a45d328fb19c451baec5090976718ea7')

def get_top_stories():
    top_headlines = newsapi.get_top_headlines(language='en', page_size=10)
    return top_headlines['articles']
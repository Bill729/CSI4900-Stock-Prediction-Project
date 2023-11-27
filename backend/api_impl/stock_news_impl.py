from newsapi import NewsApiClient
from pprint import pprint
from api_impl import stock_info_impl

NEWS_API_KEY = "e3392b1a2aa247d1900ee323aac46719"

def get_stock_news(ticker):
    newsapi = NewsApiClient(api_key = NEWS_API_KEY)
    stock_name = stock_info_impl.get_stock_name(ticker)
    
    phrase = f"{stock_name} AND Stock"
    newsapi_output = newsapi.get_everything(q=phrase,
                                language="en",
                                page_size=50)

    articles = []
    for article in newsapi_output['articles']:
        if stock_name in article["title"]:
            article["source"] = article["source"]["name"]
            del article["description"]
            del article["content"]
            articles.append(article)
    
    return articles

# Used for standalone testing, 
if __name__ == "__main__":
    get_stock_news("AAPL")
import requests
from datetime import datetime, timedelta
# from decouple import config
from dotenv import load_dotenv
import os
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news_articles():
    # 昨日の日付範囲を取得（ISO形式）
    yesterday = datetime.utcnow() - timedelta(days=1)
    from_date = yesterday.strftime('%Y-%m-%d')
    to_date = from_date  # 同じ日付を指定

    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'technology',  # 任意のキーワード
        'from': from_date,
        'to': to_date,
        'language': 'en',
        'sortBy': 'popularity',
        'pageSize': 3,
        'apiKey': NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print('NewsAPIへの接続に失敗しました。')
        return []

    articles = response.json().get('articles', [])

    # 記事の情報を整形して返す
    result = [
        {
            'title': article['title'],
            'url': article['url'],
            'source': article['source']['name'],
            'published_at': article['publishedAt']
        }
        for article in articles
    ]

    return result


if __name__ == "__main__":
    news_articles = get_news_articles()
    for i, article in enumerate(news_articles, start=1):
        print(f"{i}. {article['title']}")
        print(f"   {article['url']} ({article['source']})")
        print(f"   投稿日: {article['published_at']}")
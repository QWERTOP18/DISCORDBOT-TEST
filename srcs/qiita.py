import requests
from datetime import datetime, timedelta
# from decouple import config
from dotenv import load_dotenv
import os
load_dotenv()
QIITA_TOKEN = os.getenv("QIITA_TOKEN")

def get_qiita_articles():
    # 昨日の日付をISO 8601形式に変換
    yesterday = datetime.utcnow() - timedelta(days=1)
    yesterday_iso = yesterday.strftime('%Y-%m-%dT00:00:00+00:00')

    headers = {
        'Authorization': f'Bearer {QIITA_TOKEN}'
    }

    params = {
        'per_page': 100,
        'page': 1
    }

    response = requests.get('https://qiita.com/api/v2/items', headers=headers, params=params)

    if response.status_code != 200:
        print('Qiita APIへの接続に失敗しました。')
        return []

    items = response.json()

    # 昨日投稿された記事だけに絞る
    filtered = [
        item for item in items
        if item['created_at'] >= yesterday_iso
    ]

    # LGTM数でソートして上位3件を抽出
    top3 = sorted(filtered, key=lambda x: x['likes_count'], reverse=True)[:3]

    # 結果の整形
    result = [
        {
            'title': item['title'],
            'url': item['url'],
            'likes_count': item['likes_count']
        }
        for item in top3
    ]

    return result



if __name__ == "__main__":
    qiita_articles = get_qiita_articles()
    for i, article in enumerate(qiita_articles, start=1):
        print(f"{i}. {article['title']} ({article['likes_count']} likes)")
        print(f"   {article['url']}")
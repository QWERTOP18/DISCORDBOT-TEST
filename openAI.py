from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta, timezone
import pytz

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_chatgpt_response(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

async def extract_event_info(message: str) -> dict:
    try:
        jst = timezone(timedelta(hours=+9))
        today = datetime.now(jst).strftime("%Y-%m-%d")
        system_prompt = f"""あなたはイベント情報を抽出する専門家です。
以下の日本語メッセージからイベント情報をJSONで抽出してください：

{{
  "date": "YYYY-MM-DD",             // 日付。なければnull。
  "time": "HH:MM",                  // 時刻（24h形式）。なければnull。
  "is_relative": true|false,       // 「明日」「来週」など相対日付ならtrue。
  "relative_type": "tomorrow"|"next_day"|"next_week"|"next_month"|"date"|null,
  "description": "自然な説明文",
  "title": "イベント名（日時除く30文字以内）"
}}

【変換ルール】
- 相対表現（明日、明後日、来週、来月など）は現在日付 {today} を基準に計算。
- 曖昧な時刻（例: 夜）は補完、なければnull。
- date, time, relative_typeは見つからなければnull。
- JSON文字列のみ返してください。
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            response_format={ "type": "json_object" }
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"イベント情報抽出エラー: {e}")
        return None

if __name__ == "__main__":
    question = "こんにちは"
    response = asyncio.run(get_chatgpt_response(question))
    print(response)
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_chatgpt_response(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"



if __name__ == "__main__":
    question = "こんにちは"
    response = asyncio.run(get_chatgpt_response(question))
    print(response)
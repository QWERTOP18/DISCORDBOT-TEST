import discord
from srcs.news import get_news_articles
from srcs.qiita import get_qiita_articles
from srcs.hack1 import announce_event_info

async def handle_mention(message, bot):
    # ボット自身のメッセージは無視
    if message.author == bot.user:
        return

    # メンションされているかチェック
    if bot.user.mentioned_in(message):
        # メッセージの内容を小文字に変換して判定
        content = message.content.lower()
        
        if 'news' in content or 'ニュース' in content:
            # ニュース記事を取得
            articles = get_news_articles()
            if articles:
                response = "📰 最新のテクノロジーニュース\n\n"
                for article in articles:
                    response += f"• {article['title']}\n"
                    response += f"  ソース: {article['source']}\n"
                    response += f"  URL: {article['url']}\n\n"
                await message.channel.send(response)
            else:
                await message.channel.send("ニュースの取得に失敗しました。")
                
        elif 'qiita' in content or 'キータ' in content:
            # Qiita記事を取得
            articles = get_qiita_articles()
            if articles:
                response = "📝 人気のQiita記事\n\n"
                for article in articles:
                    response += f"• {article['title']} ({article['likes_count']} likes)\n"
                    response += f"  URL: {article['url']}\n\n"
                await message.channel.send(response)
            else:
                await message.channel.send("Qiita記事の取得に失敗しました。")
        
        elif 'event' in content or 'イベント' in content:
            # イベント情報を表示
            await announce_event_info(message, bot)
        
        else:
            # デフォルトの応答
            await message.channel.send(
                "こんにちは！以下のコマンドが使えます：\n"
                "- `news` または `ニュース`: 最新のテクノロジーニュースを表示\n"
                "- `qiita` または `キータ`: 人気のQiita記事を表示\n"
                "- `event` または `イベント`: 次のイベント情報と2025年6月4日までのカウントダウンを表示"
            ) 
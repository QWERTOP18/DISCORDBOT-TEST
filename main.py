import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import os
# from openAI import get_chatgpt_response
from datetime import datetime, timedelta
import urllib.parse

from reaction import handle_reaction
from srcs.news import get_news_articles
from srcs.qiita import get_qiita_articles
from srcs.mention import handle_mention

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ボットの起動時の設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容を読み取る権限
intents.reactions = True        # リアクションを読み取る権限
intents.guild_scheduled_events = True  # イベントを読み取る権限

bot = commands.Bot(command_prefix='/', intents=intents)

# ボットの起動時の処理
@bot.event
async def on_ready():
    print('ログインしました')
    try:
        synced = await bot.tree.sync()
        print(f"同期したコマンド: {len(synced)}")
    except Exception as e:
        print(f"同期エラー: {e}")

# リアクション追加時の処理
@bot.event
async def on_reaction_add(reaction, user):
    await handle_reaction(reaction, user)

# @bot.tree.command(name="chatgpt", description="chatgptを使って質問をします")
# @app_commands.describe(question="質問内容")
# async def chatgpt(interaction: discord.Interaction, question: str):
#     # 処理中であることを示すメッセージを送信
#     await interaction.response.defer()
    
#     # ChatGPTから応答を取得
#     response = await get_chatgpt_response(question)
    
#     # 応答を送信
#     await interaction.followup.send(f'質問: {question}\n\n回答: {response}')

# /ping
@bot.tree.command(name="ping", description="ボットの応答を確認します")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

# /schedule
@bot.tree.command(name="schedule", description="スケジュールを表示します")
@app_commands.describe(
    date="日付 (YYYY-MM-DD形式)",
    time="時間 (HH:MM形式)",
    title="タイトル",
    description="説明"
)
async def schedule(interaction: discord.Interaction, date: str, time: str, title: str, description: str = ""):
    try:
        # 日付と時間を結合してdatetimeオブジェクトを作成
        event_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        
        # Google Calendar URLを生成
        event_title_encoded = urllib.parse.quote(title)
        start_time = event_datetime.strftime('%Y%m%dT%H%M%S')
        end_time = (event_datetime + timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')
        description_encoded = urllib.parse.quote(description)
        
        calendar_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={event_title_encoded}&dates={start_time}/{end_time}&details={description_encoded}"
        
        # 埋め込みメッセージを作成
        embed = discord.Embed(
            title="📅 Google Calendar イベント",
            description=f"以下のURLからイベントを追加できます：\n[Google Calendarで開く]({calendar_url})",
            color=discord.Color.blue()
        )
        embed.add_field(name="イベントタイトル", value=title, inline=True)
        embed.add_field(name="イベント日時", value=event_datetime.strftime('%Y年%m月%d日 %H:%M'), inline=True)
        embed.add_field(name="説明", value=description, inline=True)
        
        await interaction.response.send_message(embed=embed)
        
    except ValueError as e:
        await interaction.response.send_message(
            "日付または時間の形式が正しくありません。\n"
            "日付は YYYY-MM-DD 形式（例: 2024-03-20）\n"
            "時間は HH:MM 形式（例: 15:30）で入力してください。",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            "イベントの作成中にエラーが発生しました。",
            ephemeral=True
        )

# メンション時の処理
@bot.event
async def on_message(message):
    await handle_mention(message, bot)
    # コマンドの処理を継続するために必要
    await bot.process_commands(message)

keep_alive()
bot.run(DISCORD_TOKEN)

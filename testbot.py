import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from openAI import get_chatgpt_response

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ボットの起動時の設定
intents = discord.Intents.all()
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

@bot.tree.command(name="chatgpt", description="chatgptを使って質問をします")
@app_commands.describe(question="質問内容")
async def chatgpt(interaction: discord.Interaction, question: str):
    # 処理中であることを示すメッセージを送信
    await interaction.response.defer()
    
    # ChatGPTから応答を取得
    response = await get_chatgpt_response(question)
    
    # 応答を送信
    await interaction.followup.send(f'質問: {question}\n\n回答: {response}')

# スラッシュコマンドの例: /hello
@bot.tree.command(name="hello", description="挨拶をします")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'こんにちは、{interaction.user.name}さん！')

# スラッシュコマンドの例: /ping
@bot.tree.command(name="ping", description="ボットの応答を確認します")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')

# 数値を引数に取るコマンド: /dice
@bot.tree.command(name="dice", description="サイコロを振ります")
@app_commands.describe(sides="サイコロの面の数（デフォルト: 6）")
async def dice(interaction: discord.Interaction, sides: int = 6):
    import random
    result = random.randint(1, sides)
    await interaction.response.send_message(f'🎲 {result}が出ました！')

# 文字列を引数に取るコマンド: /echo
@bot.tree.command(name="echo", description="メッセージを繰り返します")
@app_commands.describe(message="繰り返すメッセージ")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f'📢 {message}')

# 複数の引数を取るコマンド: /calc
@bot.tree.command(name="calc", description="簡単な計算をします")
@app_commands.describe(
    num1="1つ目の数字",
    num2="2つ目の数字",
    operation="演算子（+、-、*、/）"
)
async def calc(interaction: discord.Interaction, num1: float, num2: float, operation: str):
    result = None
    if operation == '+':
        result = num1 + num2
    elif operation == '-':
        result = num1 - num2
    elif operation == '*':
        result = num1 * num2
    elif operation == '/':
        if num2 == 0:
            await interaction.response.send_message('❌ 0で割ることはできません！')
            return
        result = num1 / num2
    else:
        await interaction.response.send_message('❌ 無効な演算子です。+、-、*、/ のいずれかを使用してください。')
        return
    
    await interaction.response.send_message(f'計算結果: {num1} {operation} {num2} = {result}')

bot.run(DISCORD_TOKEN)

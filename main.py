import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import os
# from openAI import get_chatgpt_response
from datetime import datetime
import calendar

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ボットの起動時の設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容を読み取る権限
intents.reactions = True        # リアクションを読み取る権限
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

# @bot.tree.command(name="chatgpt", description="chatgptを使って質問をします")
# @app_commands.describe(question="質問内容")
# async def chatgpt(interaction: discord.Interaction, question: str):
#     # 処理中であることを示すメッセージを送信
#     await interaction.response.defer()
    
#     # ChatGPTから応答を取得
#     response = await get_chatgpt_response(question)
    
#     # 応答を送信
#     await interaction.followup.send(f'質問: {question}\n\n回答: {response}')


@bot.tree.command(name="date", description="今月のカレンダーをEmbedで表示します")
async def date(interaction: discord.Interaction):
    now = datetime.now()
    year, month, today = now.year, now.month, now.day

    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    weeks = cal.monthdayscalendar(year, month)

    # カレンダーテキスト生成
    calendar_lines = ["Su Mo Tu We Th Fr Sa"]
    for week in weeks:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            elif day == today:
                line += f"**{str(day).rjust(2)}** "
            else:
                line += f"{str(day).rjust(2)} "
        calendar_lines.append(line.strip())
    calendar_text = "\n".join(calendar_lines)

    # Embed作成
    embed = discord.Embed(
        title=f"{calendar.month_name[month]} {year}",
        description=calendar_text,
        color=discord.Color.red()  # 好きな色に変更可（例：.blue(), .green(), .gold()）
    )
    embed.set_footer(text=f"Today is {year}-{month:02d}-{today:02d}")

    await interaction.response.send_message(embed=embed)

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

@bot.event
async def on_reaction_add(reaction, user):
    # ボット自身のリアクションは無視
    if user.bot:
        return

    # メッセージのチャンネルを取得
    channel = reaction.message.channel
    
    # リアクションが🌟の場合
    if str(reaction.emoji) == '🌟':
        try:
            # メッセージの内容を取得
            message_content = reaction.message.content
            message_author = reaction.message.author.name
            
            # メッセージに添付ファイルがある場合
            attachments = []
            for attachment in reaction.message.attachments:
                attachments.append(f"添付ファイル: {attachment.url}")
            
            # DMを送信
            embed = discord.Embed(
                title="🌟 保存されたメッセージ",
                description=message_content,
                color=discord.Color.gold()
            )
            embed.add_field(name="送信者", value=message_author, inline=True)
            embed.add_field(name="チャンネル", value=channel.name, inline=True)
            
            if attachments:
                embed.add_field(name="添付ファイル", value="\n".join(attachments), inline=False)
            
            await user.send(embed=embed)
            
            # チャンネルに確認メッセージを送信
            await channel.send(f"{user.mention} さんにメッセージをDMで送信しました！", delete_after=5)
            
        except discord.Forbidden:
            await channel.send(f"{user.mention} さん、DMを送信できませんでした。DMの設定を確認してください。", delete_after=10)
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            await channel.send("メッセージの送信中にエラーが発生しました。", delete_after=5)



keep_alive()
bot.run(DISCORD_TOKEN)

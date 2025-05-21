import discord
import re
from datetime import datetime, timedelta
import urllib.parse
import json
from openAI import extract_event_info
from discord.ext import commands
from discord import app_commands

async def handle_reaction(reaction, user):
    # ボット自身のリアクションは無視
    if user.bot:
        return

    # メッセージのチャンネルを取得
    channel = reaction.message.channel

    # リアクションが🕰️の場合
    if str(reaction.emoji) == '🕰️':
        try:
            # メッセージの内容を取得
            message_content = reaction.message.content
            message_author = reaction.message.author.name
            
            # OpenAIを使用してイベント情報を抽出
            event_info = await extract_event_info(message_content)
            if event_info:
                event_data = json.loads(event_info)
                
                if event_data.get("date") and event_data.get("time"):
                    # 日付と時間を結合
                    event_datetime = datetime.strptime(f"{event_data['date']} {event_data['time']}", '%Y-%m-%d %H:%M')
                    
                    # Google Calendar URLを生成
                    event_title = event_data.get("title", "イベント")
                    event_title_encoded = urllib.parse.quote(event_title)
                    start_time = event_datetime.strftime('%Y%m%dT%H%M%S')
                    end_time = (event_datetime + timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')
                    
                    calendar_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={event_title_encoded}&dates={start_time}/{end_time}"
                    
                    # 埋め込みメッセージを作成
                    embed = discord.Embed(
                        title="📅 Google Calendar イベント",
                        description=f"以下のURLからイベントを追加できます：\n[Google Calendarで開く]({calendar_url})",
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="イベントタイトル", value=event_title, inline=True)
                    embed.add_field(name="イベント日時", value=event_datetime.strftime('%Y年%m月%d日 %H:%M'), inline=True)
                    embed.add_field(name="説明", value=event_data.get("description", "説明なし"), inline=True)
                    embed.add_field(name="元のメッセージ", value=message_content, inline=False)
                    
                    await channel.send(embed=embed)
                else:
                    await channel.send("メッセージから日時情報を抽出できませんでした。\n例: 「明日の15時にミーティング」や「2024/3/20 14:30 プロジェクト会議」などの形式で入力してください。", delete_after=10)
            else:
                await channel.send("イベント情報の抽出中にエラーが発生しました。", delete_after=5)
                
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            await channel.send("イベントの作成中にエラーが発生しました。", delete_after=5)
    
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




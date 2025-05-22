import discord
from datetime import datetime, date, timezone, timedelta
from discord.ext import commands

async def get_next_event(guild):
    """ギルドの次のイベントを取得する"""
    try:
        # ギルドのイベントを取得
        events = await guild.fetch_scheduled_events()
        if not events:
            return None
        
        # 現在時刻をUTCで取得
        now = datetime.now(timezone.utc)
        upcoming_events = [event for event in events if event.start_time > now]
        
        if not upcoming_events:
            return None
            
        # 最も近いイベントを返す
        return min(upcoming_events, key=lambda x: x.start_time)
    except Exception as e:
        print(f"イベントの取得中にエラーが発生しました: {e}")
        return None

def calculate_days_until(target_date):
    """指定された日付までの残り日数を計算する"""
    today = date.today()
    target = date(2025, 6, 4)
    delta = target - today
    return delta.days

async def announce_event_info(message, bot):
    """イベント情報とカウントダウンをアナウンスする"""
    try:
        # 次のイベントを取得
        next_event = await get_next_event(message.guild)
        
        # カウントダウンの計算
        days_until = calculate_days_until(date(2025, 6, 4))
        
        response = "📅 イベント情報\n\n"
        
        if next_event:
            # UTCからJSTに変換（+9時間）
            jst_start_time = next_event.start_time.astimezone(timezone(timedelta(hours=9)))
            response += f"次のイベント: {next_event.name}\n"
            response += f"開始日時: {jst_start_time.strftime('%Y年%m月%d日 %H:%M')}\n"
            if next_event.description:
                response += f"説明: {next_event.description}\n"
            response += f"場所: {next_event.location or 'オンライン'}\n\n"
        else:
            response += "予定されているイベントはありません。\n\n"
        
        response += f"🎯 2025年6月4日まであと {days_until} 日です！"
        
        await message.channel.send(response)
        
    except Exception as e:
        await message.channel.send(f"イベント情報の取得中にエラーが発生しました: {str(e)}")

import discord
import feedparser
import asyncio
import os
from discord.ext import tasks, commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = int(os.getenv("YOUR_CHANNEL_ID"))
RSS_URL = "https://www.coindesk.com/arc/outboundfeeds/rss/"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    fetch_news.start()

@tasks.loop(minutes=15)
async def fetch_news():
    feed = feedparser.parse(RSS_URL)
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        for entry in feed.entries[:3]:
            embed = discord.Embed(title=entry.title, url=entry.link, description=entry.summary[:200] + "...", color=0x00ff00)
            embed.set_footer(text="📰 Source: Coindesk")
            await channel.send(embed=embed)
            await asyncio.sleep(2)

bot.run(os.getenv("YOUR_BOT_TOKEN"))

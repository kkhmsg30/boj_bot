import discord
from discord.ext import commands
import baekjoon
from dotenv import load_dotenv
from pathlib import Path
import os

# load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')

bot_token=os.getenv('BOT_TOKEN')
bot_log=os.getenv('PROBLEM_LOG')


intents=discord.Intents.default()
intents.message_content=True

bot=commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    print("봇이 온라인으로 전환되었습니다.")

@bot.command(name='경민아')
async def _경민아(ctx,*args):
    if ctx.author == bot.user:
        return
    if ctx.channel.id==bot_log:
        await ctx.message.delete()
        return
    await baekjoon._경민아(ctx, args)


bot.run(bot_token)
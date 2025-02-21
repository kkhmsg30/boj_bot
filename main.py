import discord
from discord.ext import commands
from boj import BOJ
from dotenv import load_dotenv
from pathlib import Path
import os
import asyncio

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / '.env')

async def start():
    bot_token=os.getenv('BOT_TOKEN')

    intents=discord.Intents.all()
    
    async with commands.Bot(command_prefix='', intents=intents) as bot:
        @bot.event
        async def on_ready():
            print("bot ready")
            
        await bot.add_cog(BOJ(bot))
        await bot.start(bot_token)

if __name__=="__main__":
    from gpt import generate_encouragement
    print(generate_encouragement())
    # asyncio.run(start())
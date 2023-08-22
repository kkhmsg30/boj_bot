import discord
from discord.ext import commands
import baekjoon

intents=discord.Intents.default()
intents.message_content=True

bot=commands.Bot(command_prefix='', intents=intents)

token = r"MTAwNTA2MjY5NTY5MjgwNDExNg.GvrngO.ia"+r"NYmyKUyMLVnu9_2d2Oyf5Oia4Rx95J2aAtIU" # 앵글리에

bot_log=baekjoon.bot_log # 앵글리에의 기억

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


bot.run(token)
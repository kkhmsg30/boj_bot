import http.client
import json
import discord
from discord.ext import commands, tasks
import random
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
from pathlib import Path
import os

boj_id={384563841146683402: "kkhmsg30", 383225124498702338: "tndyd0706"}

격려메세지=["정말 못푸시네유!", "다음에는 더 잘 풀어봐요", "기다리면서 치킨 다섯마리 먹었자나유"]

tier_image_urls=[None]+['https://media.discordapp.net/attachments/1006707877400031283/1006719572541460611/1.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719572918939740/2.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719573283831878/3.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719573661339668/4.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719574189813880/5.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719574747660308/6.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719575318073465/7.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719575825592350/8.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719576320528454/9.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719576769310850/10.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835716241772635/11.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835716573106247/12.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835716900270200/13.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835717168713778/14.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835717856563200/15.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835718263422976/16.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835718682845235/17.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835719001604127/18.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835719383302154/19.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835719773360158/20.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835800291422219/21.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835800786337822/22.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835801075753000/23.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835801419690015/24.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835801738444800/25.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835802090774558/26.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835802455683162/27.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835802799607848/28.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835803181297674/29.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835803600719892/30.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835825843118150/31.png?width=397&height=508']


def get_profile_by_id(id):
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", "/api/v3/user/show?handle="+id, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_problems_from_query(query):
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", r"/api/v3/search/problem?query="+query, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def is_solved(problem, id):
    conn = http.client.HTTPSConnection("solved.ac")
    headers = { 'Content-Type': "application/json" }
    conn.request("GET", f"/api/v3/search/problem?query=id%3A{problem}%20s%40{id}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return bool(json.loads(data.decode("utf-8"))['count'])

class SubjectView(discord.ui.View):
    def __init__(self, today, problem_log, add_problem_all_members):
        super().__init__()
        self.today=today
        self.problem_log=problem_log
        self.add_problem_all_members=add_problem_all_members

    tags={
        'None':r'%20',
        '수학':r'%23math',
        '구현':r'%23implementation',
        '다이나믹 프로그래밍':r'%23dp',
        '그래프 이론':r'%23graphs',
        '자료 구조':r'%23data_structures',
        '그리디 알고리즘':r'%23greedy'
        }

    @discord.ui.select(
        placeholder='Choose a tag',
        options=[
            discord.SelectOption(label='None'),
            discord.SelectOption(label='Random'),
            discord.SelectOption(label='수학'),
            discord.SelectOption(label='구현'),
            discord.SelectOption(label='다이나믹 프로그래밍'),
            discord.SelectOption(label='그래프 이론'),
            discord.SelectOption(label='자료 구조'),
            discord.SelectOption(label='그리디 알고리즘')
            ]
        )
    async def select_callback(self,interaction,select):
        option=select.values[0]
        if option=='Random':
            option=['수학', '구현', '다이나믹 프로그래밍', '그래프 이론', '자료 구조', '그리디 알고리즘'][random.randint(0,5)]
        subject=SubjectView.tags[option]
        tier=[r'*p5..p2']
        solvednum=r's%23100..'
        lang=r'lang%3Ako'
        solvable=r'solvable%3Atrue'
        ids=[r'!s%40kkhmsg30', r'!s%40tndyd0706', r'!s%40dandelion51']
        tagswithout=[r'!%23case_work']
        etc=r'&page=1&sort=random'

        problems=set()
        while len(problems)<len(tier):
            problems=set()
            for t in tier:
                query=r'%20'.join([subject,t,solvednum,lang,solvable]+tagswithout+ids)+etc
                data=get_problems_from_query(query)
                if not data:
                    select.disable=True
                    await interaction.response.edit_message(embed='문제가 없는데유?', view=self)
                problems.add((data['items'][0]['titleKo'],data['items'][0]['problemId']))
            
        description='\n'.join(f'**{p[0]}** - [{p[1]}](https://www.acmicpc.net/problem/{p[1]})\n' for p in problems)
        description+=f'\n\n tag : ||```{option:^20}```||'
        
        embed=discord.Embed(title='오늘의 문제', description=description)
        
        await interaction.response.edit_message(content=self.today, embed=embed, view=None)
        await interaction.guild.get_channel(self.problem_log).send(content=self.today, embed=embed)

        for p in problems:
            await self.add_problem_all_members(p)

class AdditionalProblem(discord.ui.View):
    def __init__(self, additional_problem_log, today):
        super().__init__()
        self.additional_problem_log=additional_problem_log
        self.today=today

    tags={
        'None':r'%20',
        '수학':r'%23math',
        '구현':r'%23implementation',
        '다이나믹 프로그래밍':r'%23dp',
        '그래프 이론':r'%23graphs',
        '자료 구조':r'%23data_structures',
        '그리디 알고리즘':r'%23greedy'
        }

    @discord.ui.select(
        placeholder='Choose a tag',
        options=[
            discord.SelectOption(label='Cancel'),
            discord.SelectOption(label='None'),
            discord.SelectOption(label='수학'),
            discord.SelectOption(label='구현'),
            discord.SelectOption(label='다이나믹 프로그래밍'),
            discord.SelectOption(label='그래프 이론'),
            discord.SelectOption(label='자료 구조'),
            discord.SelectOption(label='그리디 알고리즘')
            ]
        )
    async def select_callback(self,interaction,select):
        if interaction.data['values'][0]=='Cancel':
            await interaction.message.delete()
            return
        subject=SubjectView.tags[interaction.data['values'][0]]
        tier=r'*p5..p2'
        solvednum=r's%23100..'
        lang=r'lang%3Ako'
        solvable=r'solvable%3Atrue'
        ids=[r'!s%40kkhmsg30', r'!s%40tndyd0706', r'!s%40dandelion51']
        tagswithout=[r'!%23case_work']
        etc=r'&page=1&sort=random'

        
        query=r'%20'.join([subject,tier,solvednum,lang,solvable]+tagswithout+ids)+etc
        data=get_problems_from_query(query)
        p=(data['items'][0]['titleKo'],data['items'][0]['problemId'])

        description=f'**{p[0]}** - [{p[1]}](https://www.acmicpc.net/problem/{p[1]})\n'
        
        messages=[m async for m in interaction.guild.get_channel(self.additional_problem_log).history(limit=3)]
        for m in messages:
            if m.content==f'{self.today} {interaction.user}':
                embed=discord.Embed(title='오늘의 추가문제', description=m.embeds[0].description+'\n'+description)
                await interaction.response.edit_message(content=f'{self.today} {interaction.user}', embed=embed, view=None)
                await m.edit(content=f'{self.today} {interaction.user}', embed=embed)
                return
        embed=discord.Embed(title='오늘의 추가문제', description=description)
        
        await interaction.response.edit_message(content=f'{self.today} {interaction.user}', embed=embed, view=None)
        await interaction.guild.get_channel(self.additional_problem_log).send(content=f'{self.today} {interaction.user}', embed=embed)

class BOJ(commands.Cog):
    def __init__(self, bot:commands.bot):
        super().__init__()
        self.bot = bot
        
        # load environment variables
        BASE_DIR = Path(__file__).resolve().parent.parent

        load_dotenv(BASE_DIR / '.env')

        self.problem_log=int(os.getenv('PROBLEM_LOG'))
        self.additional_problem_log=int(os.getenv('ADDITIONAL_PROBLEM_LOG'))
        self.announce_channel=int(os.getenv('ANNOUNCE_CHANNEL'))
        self.solver_role=int(os.getenv('SOLVER_ROLE'))
        
        self.problems=[]

    async def add_problem_all_members(self, problem):
        for member in self.bot.guilds[0].get_role(self.solver_role).members:
            self.problems.append((member.id, problem))
        if not self.check.is_running():
            self.check.start()
        

    @commands.command()
    async def 경민아(self, ctx, *args):
        if ctx.channel.id==self.problem_log:
            await ctx.message.delete()
            return
        try:
            if random.randint(1,200)==1:
                await ctx.reply('헹?')
                return

            # 비어있을때
            if args==():
                await ctx.reply('흥! 어쩌라구요!')
                return
            
            # 세 문제 정하기
            if args==('문제줘',):
                today=datetime.now(timezone('Asia/Seoul')).strftime(r"%Y%m%d")
                messages=[m async for m in ctx.guild.get_channel(self.problem_log).history(limit=1)]
                if messages[0].content==today:
                    await ctx.reply('아까 알려줬자나유!', embed=messages[0].embeds[0], view=discord.ui.View.from_message(messages[0]))
                else:
                    await ctx.reply(view=SubjectView(today=today, problem_log=self.problem_log, add_problem_all_members=self.add_problem_all_members))
                return
            
            # 추가 문제
            if ''.join(args)=='문제더줘' or ''.join(args)=='더줘':
                today=datetime.now(timezone('Asia/Seoul')).strftime(r"%Y%m%d")
                await ctx.reply(view=AdditionalProblem(additional_problem_log=self.additional_problem_log, today=today))
                return

            # 풀었는지 판별하기
            if len(args)==3 and (args[2]=='풀었어'):
                if is_solved(args[0], args[1]) or is_solved(args[1], args[0]):
                    await ctx.reply('진짜넹')
                else:
                    await ctx.reply('거짓말 치지 마유!')
                return

            # 백준 프로필 정보
            if len(args)==2 and (args[1]=='티어' or args[1]=='정보' or args[1]=='프로필'):
                data=get_profile_by_id(args[0])

                embed=discord.Embed(title=args[0])
                embed.add_field(name="맞은 문제",value=f"{data['solvedCount']}")
                embed.add_field(name="레이팅",value=f"{data['rating']}")
                embed.set_thumbnail(url=tier_image_urls[data['tier']])

                await ctx.reply(embed=embed)
                return

            # 고마워
            if args==('고마워',):
                await ctx.reply('흥 문제나 풀어유!')
                return

        except Exception as e:
            await ctx.reply('흥! 코드 제대로 짜세유!\nError:'+str(e))

    @tasks.loop(seconds=5.0)
    async def check(self):
        try:
            print("loop", self.problems)
            today=datetime.now(timezone('Asia/Seoul')).strftime(r"%Y%m%d")
            messages=[m async for m in self.bot.guilds[0].get_channel(self.problem_log).history(limit=1)]
            if messages[0].content==today and self.problems:
                newproblems=[]
                for user, problem in self.problems:
                    if is_solved(problem[1], boj_id[user]):
                        embed=discord.Embed(title='오늘의 문제', description=f'{problem[0]} - [{problem[1]}](https://www.acmicpc.net/problem/{problem[1]})')
                        await self.bot.guilds[0].get_channel(self.announce_channel).send(content=f'이제야 풀었네유 <@{user}>\n{격려메세지[random.randint(0,len(격려메세지)-1)]}', embed=embed)
                    else:
                        newproblems.append((user,problem))
                self.problems=newproblems
                            
            else:
                print(messages[0].content, today)
                print(self.problems)
                self.problems.clear()
                self.check.cancel()
        except Exception as e:
            print(e)

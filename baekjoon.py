import http.client
import json
import discord
import random
from datetime import datetime
from pytz import timezone


tier_image_urls=[None]+['https://media.discordapp.net/attachments/1006707877400031283/1006719572541460611/1.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719572918939740/2.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719573283831878/3.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719573661339668/4.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719574189813880/5.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719574747660308/6.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719575318073465/7.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719575825592350/8.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719576320528454/9.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006719576769310850/10.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835716241772635/11.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835716573106247/12.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835716900270200/13.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835717168713778/14.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835717856563200/15.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835718263422976/16.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835718682845235/17.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835719001604127/18.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835719383302154/19.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835719773360158/20.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835800291422219/21.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835800786337822/22.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835801075753000/23.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835801419690015/24.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835801738444800/25.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835802090774558/26.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835802455683162/27.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835802799607848/28.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835803181297674/29.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835803600719892/30.png?width=397&height=508','https://media.discordapp.net/attachments/1006707877400031283/1006835825843118150/31.png?width=397&height=508']
bot_log=1006707877400031283 # 앵글리에의 기억
additional_problem=1022408326841114675


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
            discord.SelectOption(label='수학'),
            discord.SelectOption(label='구현'),
            discord.SelectOption(label='다이나믹 프로그래밍'),
            discord.SelectOption(label='그래프 이론'),
            discord.SelectOption(label='자료 구조'),
            discord.SelectOption(label='그리디 알고리즘')
            ]
        )
    async def select_callback(self,interaction,select):
        subject=SubjectView.tags[interaction.data['values'][0]]
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
                problems.add((data['items'][0]['titleKo'],data['items'][0]['problemId']))

        description='\n'.join(f'**{p[0]}** - [{p[1]}](https://www.acmicpc.net/problem/{p[1]})\n' for p in problems)
        description+=f'\n\n tag : ||{select.values[0]}||'
        
        embed=discord.Embed(title='오늘의 문제', description=description)
        
        await interaction.response.edit_message(content=today, embed=embed, view=None)
        await interaction.guild.get_channel(bot_log).send(content=today, embed=embed)

class AdditionalProblem(discord.ui.View):
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
        global today
        today=datetime.now(timezone('Asia/Seoul')).strftime(r"%Y%m%d")
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
        
        today=datetime.now(timezone('Asia/Seoul')).strftime(r"%Y%m%d")
        messages=[m async for m in interaction.guild.get_channel(additional_problem).history(limit=3)]
        for m in messages:
            if m.content==f'{today} {interaction.user}':
                embed=discord.Embed(title='오늘의 추가문제', description=m.embeds[0].description+'\n'+description)
                await interaction.response.edit_message(content=f'{today} {interaction.user}', embed=embed, view=None)
                await m.edit(content=f'{today} {interaction.user}', embed=embed)
                return
        embed=discord.Embed(title='오늘의 추가문제', description=description)
        
        await interaction.response.edit_message(content=f'{today} {interaction.user}', embed=embed, view=None)
        await interaction.guild.get_channel(additional_problem).send(content=f'{today} {interaction.user}', embed=embed)

class ProblemTypeView(discord.ui.View):
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
        options=[
            discord.SelectOption(label='g1..p3', value='*g1..p3')
            ]
        )
    async def select1_callback(self,interaction,select):
        pass

    @discord.ui.button(label='설정 완료')
    async def button_callback(self,interaction,button):
        pass

    
async def _경민아(ctx, args):
    try:
        global today
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
            messages=[m async for m in ctx.guild.get_channel(bot_log).history(limit=1)]
            if messages[0].content==today:
                await ctx.reply('아까 알려줬자나유!', embed=messages[0].embeds[0], view=discord.ui.View.from_message(messages[0]))
            else:
                await ctx.reply(view=SubjectView())
            return
        
        # 추가 문제
        if ''.join(args)=='문제더줘' or ''.join(args)=='더줘':
            await ctx.reply(view=AdditionalProblem())
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
import discord
import os
import httpx
import time, datetime
import random

from discord.ext import commands
from utils import config, errorHandler, himekawaHandler
from utils.intHandler import statusValues

bot = commands.Bot(command_prefix=config.prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    os.system('CLS')
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    await bot.load_extension("utils.errorHandler")
    bot.remove_command("help")
    await bot.change_presence(status=discord.Status.idle, 
                              activity=discord.Activity(type=discord.ActivityType.watching, 
                              name="something"))  

    if bot.user.bot != True:
        print(f'You are not running on a bot account. ({bot.user})')

    elif config.debug == '1':                           
        print(f'Bot is running on {bot.user} ({bot.user.id} | {bot.user.bot} | {bot.user.created_at})')
        print(f'This useless machine is sponsored by Insurance Gang ✉')
        print(f'I am in love with thick thighed femboys')

    else:
        print(f'This useless machine is sponsored by Insurance Gang ✉')
        print(f'I am in love with thick thighed femboys')

@bot.command(aliases=['check', 'checkrank'])
async def check_ranked(ctx, username):
    role = discord.utils.get(ctx.author.guild.roles, name="ranked")
    
    async with httpx.AsyncClient() as client:
        user_res = await client.get(f"https://osu.ppy.sh/api/get_user?u={username}&k={config.osukey}")
        user_data = user_res.json()
        if not user_data:
            await ctx.send("**Request failed** (Restricted/invalid username)")
            return
            
        beatmaps_res = await client.get(f"https://osu.ppy.sh/api/get_beatmaps?u={username}&since=1999-01-01&k={config.osukey}")
        data = beatmaps_res.json()

    if not data:
        await ctx.send("**Request failed** (No maps)")
        return
        
    with open("./misc/users.txt") as f:
        if username in f.read():
            print(f"[{username}] Repeat user found")
            await ctx.send(f"**You have already verified**, {username}")
            return

        msg = await ctx.send("*Checking your maps...*")
            
        for i in data:
            if i['approved'] != '1':
                if config.debug == '1':
                    bid = i['beatmapset_id']
                    app = i['approved']
                    status = statusValues[app]
                    print(f"{username} | {bid} | {app} ({status})")
                    continue
                        
                else:
                    continue
                        
            elif i['approved'] == '1':
                await ctx.author.add_roles(role)
                await msg.edit(content=f"Ranked map found! You have received your role, **{username}**.")
                print(f"{username} | Ranked map found - giving role")
                return

    await msg.edit(content=f"You do **not** have any ranked maps, {username}.")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! Took {0}ms.'.format(round(bot.latency, 4)))

@bot.command()
async def himekawa(ctx):
    await ctx.send(random.choice(himekawaHandler.himePhrases))

@bot.command()
async def about(ctx):
    await ctx.send("This was brought to you by LUNA :D\nI made this whole bot in about 3 hours and I'm gonna keep adding to it so I hope you all like the features\nAlso do .himekawa if you haven't already :-)")

bot.run(config.token)
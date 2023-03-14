import discord
import os
import requests
import time, datetime

from discord.ext import commands
from utils import config, errorHandler
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
    req = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?u={username}&since=1999-01-01&k={config.osukey}")
    data = req.json()

    with open('./misc/users.txt') as f:
        if f'{username}' in f.read():
            print(f"[{username}] Repeat user found")
            await ctx.send("You have already verified!")
        else:
            global message
            message = await ctx.send("*Checking your maps...*")
      
    while True:
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
                await message.edit(content=f"Ranked map found! You have received your role, **{username}**.")
                print(f"{username} | Ranked map found - giving role")
                with open("./misc/users.txt", "a") as f:
                    f.write(f"\n{username}")
                break

            else:
                await message.edit(content=f"You do not have any ranked maps, {username}.")

        break

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! Took {0}ms.'.format(round(bot.latency, 4)))

@bot.command()
async def himekawa(ctx):
    await ctx.send("Every attempt at making an argument you Fail. You try to  make a map and Fail. You try doing anything and Failure is the only path you walk towards. You live a life devoid of any meaning. Stop trying to talk to me when you lack the mental fortitude to even say something tangible.")

bot.run(config.token)
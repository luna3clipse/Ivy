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
        print(f'This useless machine is sponsored by Insurance Gang')
        print(f'I am in love with thick thighed femboys')

    else:
        print(f'This useless machine is sponsored by Insurance Gang')
        print(f'I am in love with thick thighed femboys')

    global OSU_TOKEN  
    TOKEN_URL = 'https://osu.ppy.sh/oauth/token'
    
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_URL, data = config.osukey)
        OSU_TOKEN = response.json().get('access_token')
    return None
    
@bot.command(aliases=['check', 'checkrank'])
async def check_ranked(ctx, username):
    role = discord.utils.get(ctx.author.guild.roles, name="ranked")
    
    with open('./misc/users.txt') as f:
        if f'{username}' in f.read():
            print(f"[{username}] Repeat user found")
            await ctx.send("You have already verified!")
            return

    headers = {"Authorization": f"Bearer {OSU_TOKEN}"}
    
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(f'https://osu.ppy.sh/api/v2/users/{username}/osu')
        
        if response.status_code == 200:
            beatmapset_count = response.json()['ranked_beatmapset_count']

            if beatmapset_count > 0:
                await ctx.send(f":white_check_mark: {username} has **{beatmapset_count}** ranked beatmapsets!")
                await ctx.author.add_roles(role)
            else:
                await ctx.send(f"{username} does not have any ranked beatmapsets.")
        else:
            await ctx.send("Unable to retrieve user's beatmapsets.")

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! Took {0}ms.'.format(round(bot.latency, 4)))

@bot.command()
async def himekawa(ctx):
    await ctx.send(random.choice(himekawaHandler.himePhrases))

@bot.command()
async def about(ctx):
    await ctx.send("This was brought to you by LUNA :D\nI made this whole bot in about 3 hours and I'm gonna keep adding to it so I hope you all like the features\nAlso do .himekawa if you haven't already :-)")

if __name__ == "__main__":
    bot.run(config.token)
import discord
import os
import requests

from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

from discord.ext import commands
from utils import config, errorHandler, mysqlConfig

bot = commands.Bot(command_prefix=config.prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print(f'Bot is running on {bot.user}')  
    await bot.load_extension("errorHandler")   
    await bot.change_presence(status=discord.Status.online, 
                              activity=discord.Activity(type=discord.ActivityType.watching, 
                              name="something"))

@bot.command(aliases=['check', 'checkrank'])
async def check_ranked(ctx, username):
    req = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?u={username}&since=1999-01-01&k={config.osukey}")
    data = req.json()

    global message
    message = await ctx.send("*Checking your maps...*")
      
    while True:
        for i in data:
            if i['approved'] != '1':
                continue
            elif i['approved'] == '1':
                await message.edit(content=f"Ranked map found! You have received your role, **{username}**.")
                print(f"[{username}] Ranked map found - giving role")
                break
        break


bot.run(config.token)

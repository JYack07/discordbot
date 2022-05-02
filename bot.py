from http import client
import discord

import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./botstuff.env')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

bot = commands.Bot(command_prefix='//')

@bot.event
async def on_ready():
    print('Logged on as bot.py!')


@bot.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))

    if message.content.lower().startswith('hello there'):
        await message.channel.send(file=
                discord.File(fp=open('GIFs/general-kenobi.gif', 'rb')))
            
afkPeeps = {}
@bot.command(name = 'AFK')
async def afk(ctx):
    global afkPeeps
    
bot.run(DISCORD_TOKEN)

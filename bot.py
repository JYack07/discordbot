
#!/bin/python3
import discord
import os

from http import client
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv('./botstuff.env')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='$')

# Usage: //afk <reason> 
# Inserts the user into the afk_peeps dictionary, along with their reason 
# for being afk. If this user is mentioned, relay a message stating that user's
# reason.
afk_peeps = {}
@bot.command(name = 'afk')
async def afk(ctx):
    global afk_peeps
    if ctx.author not in afk_peeps.keys():
        afk_peeps[ctx.author] = ctx.message.content
    
    # Allows the user to know that the bot actually knows they're afk
    await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

   
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')

# Confirms that the bot is logged on and ready to be used                       
@bot.event                                                                      
async def on_ready():                                                           
    print('Logged on as bot.py!')                                               
                                                                                
# Checks incoming messages to passively respond based on the message. More to   
# be added.                                                                     
@bot.event                                                                      
async def on_message(message):                                                  
    print('Message from {0.author}: {0.content}'.format(message))               
        
    # A funny                                                                      
    if 'hello there' in message.content.lower():                                
        await message.channel.send(file=                                        
                discord.File(fp=open('GIFs/general-kenobi.gif', 'rb')))

    # Removes AFK when person messages in chat
    if message.author in afk_peeps:
        afk_peeps.pop(message.author)
        if str(message.author.nick) != "None":
            msg = str(message.author.nick) 
        else:
           msg = str(message.author.name)
        msg += ", your AFK has been removed."
        
        # Creates a discord rich text embed
        embed = discord.Embed(
            title="AFK Removed",
            url="",
            description=msg,
            color=discord.Color.blue())
        
        await message.channel.send(embed=embed)
    
    # When someone pings an afk user, it tells the author the reason they are afk
    for user in message.mentions:
        if user in afk_peeps:
            if str(user.nick) != "None":
                afkmsg = str(user.nick) 
            else:
                afkmsg = str(user.name)
                
            afkmsg += " is AFK right now."
            reason = "Reason: "
            reason += str(afk_peeps[user]).replace('$afk ', '')
            
            embed=discord.Embed(
                title=afkmsg,
                url="",
                description=reason,
                color=discord.Color.blue())
            
            await message.channel.send(embed=embed)

    # Required in order for commands to be processed due to overriding 
    # on_message.
    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
#!/bin/python3
from pyexpat import ErrorString
from re import X
import discord
import os
import requests
import random
import json
import time

from http import client
from discord.ext import commands
from dotenv import load_dotenv
from PyDictionary import PyDictionary

load_dotenv('./botstuff.env')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GIF_API = os.getenv("GIF_API")

bot = commands.Bot(command_prefix='$')

vcs = {}
# Usage $ewwp_set <channel ids>
@bot.command(name="ewwp_set")
async def ewwp_set(ctx, channels:str):
    embed = discord.Embed(
                title="Could not set EWWP Channels",
                url='',
                color=discord.Color.red())
    
    # TODO: Fix channel integrity error handling
    vc_list = []
    num_vcs = 0
    while discord.Guild.voice_channels[num_vcs].name != "":
        vc_list[num_vcs] = discord.Guild.voice_channels[num_vcs].id
        num_vcs += 1

    i = 0
    c_list = channels.split(",")
    for x in c_list:
        is_valid = False
        for vc in range(len(vc_list)):
           if x == discord.Guild.voice_channels[vc].id:
               is_valid = True

        if is_valid is False:
            embed.description="Invalid Channel ID"
            await ctx.send(embed=embed)
            return

        vcs[i]=bot.get_channel(int(x))
        i = i + 1

    if i > 1:
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
    else:
        embed.description="Not enough channel arguments"
        embed.color=discord.Color.red()
        await ctx.send(embed=embed)
        vcs = {}

# Usage $ewwp <@person>
# Moves user between voice channels to be annoying or get their attention
@bot.command(name="ewwp")
@commands.has_role("Admin")
async def ewwp(ctx, member:discord.Member, *, reason=None):
    num = 5
    embed = discord.Embed(
                title="Initializing Emergency Wakey Wakey Protocol",
                description="Please stand by...",
                color=discord.Color.blue())
    
    await ctx.send(embed=embed)
    
    x = len(vcs)
    if x > 1:
        for i in range(num):
            for y in range(x):
                await member.move_to(vcs[y])
                time.sleep(0.25)

        embed = discord.Embed(
                    title="Emergency Wakey Wakey Protocol Initialized",
                    description="Wakey wakey",
                    color=discord.Color.blue())
    
    else:
        embed = discord.Embed(
                    title="Emergency Wakey Wakey Protocol Failed",
                    description="Please use ewwp_set to select voice channels",
                    color=discord.Color.red())

    await ctx.send(embed=embed)

# Usage: $kick <@person> reason
# kicks mentioned users
@bot.command(name="kick")
@commands.has_role("Admin")
async def kick(ctx, member:discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        
# ERROR FOR KICK
@kick.error
async def kick_error(ctx, error):
    print ("{0}".format(error))
    #creates embed
    embed = discord.Embed(
                title="Could Not Kick Member",
                url="",
                color=discord.Color.blue())
    
    # error checking for command errors
    if isinstance(error, commands.MissingRole):
        embed.description="Missing Admin Role"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed.description="Bot doesnt have permission"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed.description="Missing permissions"
        await ctx.send(embed=embed)

# Usage: $ban <@person> reason
# bans mentioned users
@bot.command(name="ban")
@commands.has_role("Admin")
async def ban(ctx, member:discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

# ERROR FOR BAN
@ban.error
async def ban_error(ctx, error):
    print ("{0}".format(error))
    #creates embed
    embed = discord.Embed(
                title="Could Not Ban Member",
                url="",
                color=discord.Color.blue())
    
    # error checking for command errors
    if isinstance(error, commands.MissingRole):
        embed.description="Missing Admin Role"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed.description="Bot doesnt have permission"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed.description="Missing permissions"
        await ctx.send(embed=embed)
        
# Usage: $purge <num-chats>
# Deletes num-chats amount of messages in channel used 
@bot.command(name="purge")
@commands.has_role("Admin")
async def purge(ctx, *args: int):
    # Creates embed
    embed = discord.Embed(
                title="Could Not Purge",
                url="",
                color=discord.Color.blue())
    
    # first two ifs check how many arguements are passed
    if len(args) > 1:
        embed.description="Too many arguements"
        await ctx.send(embed=embed)
    elif len(args) <= 0:
        embed.description="Not enough arguements"
        await ctx.send(embed=embed)
    
    # Last statement does the deleting
    else:
        limit = args[0]
        
        # Checks if the limit is greater than 100
        if limit > 100:
            embed.description="Integer must be less than or equal to 100"
            await ctx.send(embed=embed)
            
        # Does the deletions and sends a message
        else:
            deleted = await ctx.channel.purge(limit=limit)
            embed.title="Purge Completed"
            embed.description='Deleted {} message(s)'.format(len(deleted)) + ' by ' + ctx.message.author.mention
            
            await ctx.send(embed=embed)
        
# ERROR FOR PURGE
@purge.error
async def purge_error(ctx, error):
    print ("{0}".format(error))
    #creates embed
    embed = discord.Embed(
                title="Could Not Purge",
                url="",
                color=discord.Color.blue())
    
    # error checking for command errors
    if isinstance(error, commands.MissingRole):
        embed.description="Missing Admin Role"
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed.description="Incorrect input, please enter an integer value"
        await ctx.send(embed=embed)
        
        

# Usage: $defn <word>
# Sends the dictionary meaning of word
dictionary=PyDictionary()
@bot.command(name="defn")
async def defn(ctx, word):
    define=dictionary.meaning(word)
    word = word[0].upper() + word[1:len(word)]
    meanings = ""
    for s in define:
        meanings += "**__" + s + "__**:\n"
        for d in define[s]:
            meanings += "   - " + d + "\n"
        
    embed=discord.Embed(
        title=word + ":",
        url="",
        description=meanings,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Usage: $gif <seach_term>
# Searches for a gif using the tenor api and sends it to the chat 
# search_term is the whole string after the $gif 
@bot.command(name = 'gif')
async def gif(ctx):
    # number of gifs it can pull max
    lmt = 20
    
    # search term
    search_term = ctx.message.content.replace('$gif ', '')
    
    # get gifs from api
    r = requests.get("https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, GIF_API, lmt))

    if r.status_code == 200:
        # load top 10 gifs using urls
        top_10gifs = json.loads(r.content)
        
        gif = random.choice(top_10gifs['results'])
        await ctx.send(gif['media'][0]['gif']['url'])
    else:
        # Error Handling
        embed = discord.Embed(
            title="Could not find GIF",
            url="",
            description="Gifs could not be loaded",
            color=discord.Color.blue())
        await ctx.send(embed=embed)

# Usage: $afk <reason> 
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
    
    # When someone pings an afk user, it tells the author the reason they re afk
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

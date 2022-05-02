import discord

import os

from dotenv import load_dotenv

load_dotenv('./botstuff.env')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.author == self.user:
            return

        if message.content.lower().startswith('hello there'):
            await message.channel.send(file=
                    discord.File(fp=open('GIFs/general-kenobi.gif', 'rb')))

client = MyClient()
client.run(DISCORD_TOKEN)

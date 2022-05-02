import discord

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
client.run('OTcwNDc5NjI0MzMxMDk2MTE1.Ym8jlQ.bkDThAXsGQbedL6KxfacozL5Zac')

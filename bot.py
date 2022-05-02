import discord

class MyClient(discord.client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('OTcwNDc5NjI0MzMxMDk2MTE1.Ym8jlQ.3Cjc3keqZy6sE79qG0c6OoSPtyw')

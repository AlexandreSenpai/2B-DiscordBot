###[BUILT-IN MODULES]###

########################
###[PERSONAL MODULES]###

########################
###[EXTERNAL MODULES]###
import discord
########################

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

if __name__ == '__main__':
    client = Client()
    client.run(client.__TOKEN)
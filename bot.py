###[BUILT-IN MODULES]###
import random
import urllib.request
import io
from time import sleep
import os
########################
###[PERSONAL MODULES]###
from lib.auth import Auth
from lib.rule34 import _Rule34
from lib.YTDLSource import YTDLSource
########################
###[EXTERNAL MODULES]###
import requests
import discord
from discord import File
from discord.ext import commands
########################

client = commands.Bot(command_prefix = 'pod:')

@client.event
async def on_ready():
    print(f'Online with nickname {client.user}')

@client.command()
async def rollDice(ctx, _range):
    try:
        _range = int(_range)
        await ctx.send(f'Você tirou {random.randint(1, _range)}')
    except ValueError:
        await ctx.send('Por favor, apenas digite números após o comando de dado.')

#NSFW channel only
@client.command()
async def rule34(ctx, *search_term):
    if ctx.message.channel.nsfw:
        search_term = "+".join(search_term)
        rule = _Rule34(event_loop=client.loop)
        
        async with ctx.typing():
            image = await rule.get_url_images(search_term)
            if image != 'Nenhuma imagem encontrada':
                with urllib.request.urlopen(image) as url:
                    f = io.BytesIO(url.read())
                    await ctx.send(file=File(f, filename='image.jpg'))
            else:
                await ctx.send(image)
    else:
        await ctx.send('Este comando só está disponível para salas NSFW.')

@client.command()
async def timer(ctx, timeout):
    try:
        number = int(timeout)
        await ctx.send(f"Contando de {timeout}...")
        for num in range(0, number):
            sleep(1)
            async with ctx.typing():
                await ctx.send(f"Numero: {(number - 1) - num}")
    except ValueError:
        await ctx.send(f"Por favor, utilize apenas números.")

@client.command()
async def play(ctx, *url):
    #join
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    except Exception as exc:
        print(exc)

    #play
    query = " ".join(url)
    
    queue = []

    voice_channel = ctx.message.guild.voice_client

    if voice_channel.is_playing():
        queue.append(query)

    async with ctx.typing():
        filename, player = await YTDLSource.from_url(query, loop=client.loop)
        voice_channel.play(player, after=lambda e: print(f'Player error {e}') if e else os.remove(filename))

    await ctx.send(f'Now playing: {player.title}')

@client.command()
async def pause(ctx):
    ctx.message.guild.voice_client.pause()

@client.command()
async def resume(ctx):
    ctx.message.guild.voice_client.resume()

@client.command()
async def stop(ctx):
    ctx.message.guild.voice_client.stop()

if __name__ == '__main__':
    TOKENS = Auth()
    client.run(TOKENS.DISCORD_BOT_TOKEN)
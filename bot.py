###[BUILT-IN MODULES]###
import random
import math
import io
from time import sleep
import os
########################
###[PERSONAL MODULES]###
from lib.auth import Auth
from lib.rule34 import _Rule34
from lib.YTDLSource import YTDLSource
from lib.tools import Tools
########################
###[EXTERNAL MODULES]###
import requests
import discord
from discord import File
from discord.ext import commands
########################

###INSTANCE INIATILZING###
client = commands.Bot(command_prefix = 'pod.')
tools = Tools()
##########################

@client.event
async def on_ready():
    print(f'Online with nickname {client.user}')
############################################!!!!MODERATE!!!!####################################################
################################################################################################################
############################################!!!!JOY AND GAMES!!!!###############################################
@client.command()
async def rollDice(ctx, _range):
    try:
        _range = int(_range)
        await ctx.send(f'You gotted number {random.randint(1, _range)}')
    except ValueError:
        await ctx.send('Please, just enter number after command.')

@client.command()
async def coinflip(ctx):
    options = ['heads', 'tails']
    choice = random.randint(0, len(options) - 1)
    async with ctx.typing():
        await ctx.send(f'I flipped a coin and it landed on **{options[choice]}**.')
################################################################################################################
############################################!!!!IMAGE PROCESSING!!!!############################################
################################################################################################################
##################################################!!!!NSFW!!!!##################################################
@client.command()
async def rule34(ctx, *search_term):
    if ctx.message.channel.nsfw:
        search_term = "+".join(search_term)
        rule = _Rule34(event_loop=client.loop)
        
        async with ctx.typing():
            image = await rule.get_url_images(search_term)
            if image != None:
                image_bytes = tools.image_to_bytes(image)
                await ctx.send(file=File(image_bytes, filename='image.jpg'))
            else:
                await ctx.send(f'No images about {search_term} was found!')
    else:
        await ctx.send('This command is only allowed in NSFW chats.')
################################################################################################################
##############################################!!!!UTILITIES!!!!#################################################
@client.command()
async def timer(ctx, timeout):
    try:
        number = int(timeout)
        await ctx.send(f"Counting of {timeout}...")
        for num in range(0, number):
            sleep(1)
            async with ctx.typing():
                await ctx.send(f"Number: {(number - 1) - num}")
    except ValueError:
        await ctx.send(f"Please, input only numbers.")
@client.command(pass_context=True)
async def teamBuilder(ctx):

    active_users = [member.name for member in ctx.message.author.voice.channel.members]
    random.shuffle(active_users)
    active_users = active_users[:10]
    teams = []
    
    if len(active_users) > 2:
        
        random_index = random.randint(0, len(active_users) - 1)
        teams.append([f'*{active_users[random_index]} - Captain*'])
        del active_users[random_index]
        random_index = random.randint(0, len(active_users) - 1)
        teams.append([f'*{active_users[random_index]} - Captain*'])
        del active_users[random_index]

        random.shuffle(active_users)

        avaiable_members = len(active_users)
        team_number = math.ceil(avaiable_members / 2)
        loop_times = math.ceil(avaiable_members / team_number)

        init = 0
        final = team_number
        for loop in range(0, loop_times):
            [teams[loop].append(new_member) for new_member in active_users[init:final]]
            init += final
            final += team_number
        

    else:
        teams = [[f'*{active_users[0]} - Captain*', f'*{active_users[1]} - Captain*']]

    async with ctx.typing():
        
        blue_team = ''
        red_team = ''
        for blue_member in teams[0]:
            blue_team += blue_member + '\n'
        for red_member in teams[1]:
            red_team += red_member + '\n'

        await ctx.send(f'**Blue Team:**\n{blue_team}\n**Red Team:**\n{red_team}')

################################################################################################################
########################################!!!!MUSIC AND PLAYBACK!!!!##############################################
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

        thumb_url = player.data['thumbnails'][0]['url']
        if thumb_url:
            thumb_bytes = tools.image_to_bytes(thumb_url)
            await ctx.send(file=File(thumb_bytes, filename='thumbnail.jpg'))
        else:
            await ctx.send('this video has no thumbnails')

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
################################################################################################################

if __name__ == '__main__':
    TOKENS = Auth()
    client.run(TOKENS.DISCORD_BOT_TOKEN)
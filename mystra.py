#!/usr/bin/python

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=';')
    
@bot.command(name='hello')
@commands.has_role('Demigod')
async def hello(ctx):
    await ctx.send('Hello world!')

bot.run(TOKEN)


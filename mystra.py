#!/usr/bin/python

import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
MOD_ROLE = os.getenv('MOD_ROLE')


intents = discord.Intents.none()
intents.guilds = True
intents.members = True

description = "The stars are out and magic is here"

bot = commands.Bot(command_prefix=";", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.event
async def on_guild_available(guild):
    print(f"Connected to {guild.name}")
    print("Members:")

    for member in [m for m in guild.members if not m.bot]:
        if member.nick:
            print(f"  {member.nick} ({member.name}#{member.discriminator})")
        else:
            print(f"  {member.name}#{member.discriminator}")

    print("------")
    

@bot.command()
@commands.has_role(MOD_ROLE)
async def hello(ctx):
    await ctx.send('Hello world!')


bot.run(TOKEN)


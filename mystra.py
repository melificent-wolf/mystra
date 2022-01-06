#!/usr/bin/python

import os
import os.path
import sys

import logging
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Set up logging

log_dir = "logs"
log_filename = f"{log_dir}/mystra.log"

if not os.path.exists(log_dir):
    os.mkdir(log_dir, mode=0755)

max_log_size = 10 * 1024 * 1024
handler = RotatingFileHandler(log_filename, maxBytes=max_log_size, backupCount=4)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


# Load config

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
MOD_ROLE = os.getenv('MOD_ROLE')


intents = discord.Intents.none()
intents.guilds = True
intents.members = True

description = "The stars are out and magic is here"

bot = commands.Bot(command_prefix=";", description=description, intents=intents)

guild = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.event
async def on_guild_available(g):
    global guild
    guild = g
    print(f"Connected to {g.name}")
    print("Members:")

    for member in [m for m in g.members if not m.bot]:
        if member.nick:
            print(f"  {member.nick} ({member.name}#{member.discriminator})")
        else:
            print(f"  {member.name}#{member.discriminator}")

    print("------")
    

@bot.event
async def on_member_join(member):
    msg = f"{member.mention} has arrived.  Welcome to the Mystic Inn!  Come sit for a spell!"
    await guild.system_channel.send(msg)
    await guild.owner.send(f"{member.name} has joined")


@bot.event
async def on_member_remove(member):
    msg = f"Bye, {member.display_name}, we hope you enjoyed your stay here."
    await guild.system_channel.send(msg)


@bot.command()
@commands.has_role(MOD_ROLE)
async def hello(ctx):
    await ctx.send('Hello world!')


bot.run(TOKEN)


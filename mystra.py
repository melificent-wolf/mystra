#!/usr/bin/python

import os
import os.path

import logging
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Set up logging

log_dir = "logs"
log_filename = f"{log_dir}/mystra.log"

if not os.path.exists(log_dir):
    os.mkdir(log_dir, mode=0o755)

max_log_size = 10 * 1024 * 1024
handler = RotatingFileHandler(log_filename, maxBytes=max_log_size, backupCount=4)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


# Load config

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
MOD_ROLE = os.getenv('MOD_ROLE')
NEWCOMER_ROLE = os.getenv('NEWCOMER_ROLE')

# Create bot

intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix=";", intents=intents)

guild = None


# EVENTS


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.event
async def on_guild_available(g):
    print(f"Connected to {g.name}")
    print("------")


@bot.event
async def on_member_join(member):
    await guild.owner.send(f"{member.name}#{member.discriminator} is joining")


@bot.event
async def on_member_remove(member):
    msg = f"Bye, {member.display_name}, we hope you enjoyed your stay here."
    guild = member.guild
    await guild.system_channel.send(msg)


@bot.event
async def on_member_update(before, after):
    was_new = bool(discord.utils.get(before.roles, name=NEWCOMER_ROLE))
    is_new = bool(discord.utils.get(after.roles, name=NEWCOMER_ROLE))
    if (was_new and not is_new):
        # user has passed captcha
        msg = f"{after.mention} has arrived.  Welcome to the Mystic Inn!  Come sit for a spell!"
        guild = after.guild
        await guild.system_channel.send(msg)

# COMMANDS


@bot.command()
@commands.has_role(MOD_ROLE)
async def hello(ctx):
    await ctx.send('Hello world!')


bot.run(TOKEN)

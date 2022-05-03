#!/usr/bin/python

import os
import os.path

import logging
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands
from dotenv import load_dotenv


# Prepare to load extensions
extensions = ['commands', 'events']

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
GUILD_ID = int(os.getenv('DISCORD_GUILD'))
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
MOD_ROLE = os.getenv('MOD_ROLE')
NEWCOMER_ROLE = os.getenv('NEWCOMER_ROLE')

# Create bot

intents = discord.Intents.none()
intents.bans = True
intents.guilds = True
intents.members = True
#intents.messages = True

bot = discord.Bot(debug_guilds=[GUILD_ID], intents=intents)


@bot.slash_command(guild_ids=[GUILD_ID], name="reload", description="reload configuration")
@commands.is_owner()
async def reload(ctx):
    print("Reload command received, reloading extensions")
    for ext in extensions:
        bot.reload_extension(ext)
    await ctx.send("OK")

# Load extensions
for ext in extensions:
    bot.load_extension(ext)

bot.run(TOKEN)

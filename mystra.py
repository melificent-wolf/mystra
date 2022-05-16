#!/usr/bin/python

import os
import os.path
import sys

import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

import discord
from discord.ext import commands
from dotenv import load_dotenv


# Prepare to load extensions
extensions = ['commands', 'events']

# Set up logging

log_dir = "logs"
max_log_size = 10 * 1024 * 1024

if not os.path.exists(log_dir):
    os.mkdir(log_dir, mode=0o755)

# Log discord messages to file
discord_log_filename = f"{log_dir}/discord.log"
discord_log_format = '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
discord_handler = RotatingFileHandler(discord_log_filename, maxBytes=max_log_size, backupCount=4)
discord_handler.setFormatter(logging.Formatter(discord_log_format))
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
discord_logger.addHandler(discord_handler)

# Log mystra messages to file and stdout
mystra_log_filename = f"{log_dir}/mystra.log"
mystra_log_format = '[%(asctime)s] %(levelname)s %(message)s'
mystra_handler1 = RotatingFileHandler(mystra_log_filename, maxBytes=max_log_size, backupCount=4)
mystra_handler1.setFormatter(logging.Formatter(mystra_log_format))
mystra_handler2 = StreamHandler(stream=sys.stdout)
mystra_handler2.setFormatter(logging.Formatter(mystra_log_format))
mystra_logger = logging.getLogger("mystra")
mystra_logger.setLevel(logging.INFO)
mystra_logger.addHandler(mystra_handler1)
mystra_logger.addHandler(mystra_handler2)

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
    mystra_logger.info("Reload command received, reloading extensions")
    for ext in extensions:
        bot.reload_extension(ext)
    await ctx.respond("OK")

# Load extensions
for ext in extensions:
    bot.load_extension(ext)

bot.run(TOKEN)

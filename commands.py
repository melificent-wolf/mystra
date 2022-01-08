from discord.ext import commands
import config


cfg = config.Config()


@commands.command()
@commands.has_role(cfg.mod_role)
async def hello(ctx):
    await ctx.send('Hello world!')


def setup(bot):
    bot.add_command(hello)

from discord.ext import commands
import config

import random

cfg = config.Config()

class CommandCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.drinks = [
            'tea', 'tea', 'tea',
            'cocoa', 'cocoa',
            'coffee',
            'espresso',
            'mocha',
            'mulled cider',
            'broth',
            'ball bearings',
        ]

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def botsnack(self, ctx):
        await ctx.send(f"Thank you, {ctx.author.mention}! :)")

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def drink(self, ctx, giveto=None):
        if not giveto:
            giveto = ctx.author.mention

        drink = random.choice(self.drinks)
        await ctx.send(f"Here, {giveto}, have a nice hot relaxing cup of {drink} :coffee:")

    @commands.command()
    @commands.has_role(cfg.mod_role)
    async def hello(self, ctx):
        await ctx.send("Hello world!")


def setup(bot):
    bot.add_cog(CommandCog(bot))

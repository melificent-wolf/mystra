import discord
from discord.ext import commands
import config

import random

cfg = config.Config()

class CommandCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        bubble_tea = ":bubble_tea:"
        coffee = ":coffee:"
        cup_with_straw = ":cup_with_straw:"
        milk = ":milk:"
        mug = "<:mug:922015564883451945>"
        tea = ":tea:"
        trophy = ":trophy:"

        self.drinks = [
            ('hot', 'cup of tea', tea),
            ('hot', 'cup of tea', tea),
            ('hot', 'cup of tea', tea),
            ('hot', 'cup of cocoa', mug),
            ('hot', 'cup of cocoa', mug),
            ('hot', 'cup of coffee', coffee),
            ('hot', 'cup of espresso', mug),
            ('hot', 'cup of mocha', mug),
            ('hot', 'cup of mulled cider', mug),
            ('hot', 'cup of broth', mug),
            ('hot', 'cup of ball bearings', mug),
            ('cold', 'glass of water', cup_with_straw),
            ('cold', 'glass of milk', milk),
            ('cold', 'bubble tea', bubble_tea),
            ('cold', 'cup of ambrosia', trophy)
        ]

#    @commands.command()
#    @commands.cooldown(1, 30, commands.BucketType.user)
#    async def botsnack(self, ctx):
#        await ctx.send(f"Thank you, {ctx.author.mention}! :)")

    @commands.slash_command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def drink(self, ctx, giveto=None):
        """Give someone a drink"""
        if not giveto:
            giveto = ctx.author.mention

        drink = random.choice(self.drinks)
        (temp, beverage, emoji) = drink
        await ctx.respond(f"Here, {giveto}, have a nice {temp} relaxing {beverage} {emoji}")


def setup(bot):
    bot.add_cog(CommandCog(bot))

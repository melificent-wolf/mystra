import discord
import discord.utils
from discord.ext import commands

import config


class EventCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cfg = config.Config()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        print("------")

    @commands.Cog.listener()
    async def on_guild_available(self, guild):
        print(f"Connected to {guild.name}")
        print("------")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if not hasattr(user, "guild"):
            return

        newcomer_role = self.cfg.newcomer_role
        # the first role is @everybody
        await user.remove_roles(user.roles[1:], reason="banned")
        newcomer_role = discord.utils.get(guild.roles, self.cfg.newcomer_role)
        await user.add_roles(newcomer_role, reason="bsnned")

        msg = f"And stay out, {member.display_name}!"

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.guild.owner.send(f"{member.name}#{member.discriminator} is joining")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        newcomer_role = self.cfg.newcomer_role
        was_new = bool(discord.utils.get(member.roles, name=newcomer_role))
        if was_new:
            return

        msg = f"Bye, {member.display_name}, we hope you enjoyed your stay here."
        guild = member.guild
        await guild.system_channel.send(msg)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        newcomer_role = self.cfg.newcomer_role
        was_new = bool(discord.utils.get(before.roles, name=newcomer_role))
        is_new = bool(discord.utils.get(after.roles, name=newcomer_role))
        if (was_new and not is_new):
            # user has passed captcha
            msg = f"{after.mention} has arrived.  Welcome to the Mystic Inn!  Come sit for a spell!"
            guild = after.guild
            await guild.system_channel.send(msg)


def setup(bot):
    bot.add_cog(EventCog(bot))

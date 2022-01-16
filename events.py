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
    async def on_member_join(self, member):
        guild = member.guild
        msg = f"{member.mention} has arrived.  Welcome to the Mystic Inn!  Come sit for a spell!"

        await member.guild.owner.send(f"{member.name}#{member.discriminator} has joined")
        await guild.system_channel.send(msg)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        msg = f"Bye, {member.display_name}, we hope you enjoyed your stay here."
        banned_users = await guild.bans()

        for ban in banned_users:
            if ban.user.id == member.id:
                msg = f"And stay out, {member.display_name}!"
                break

        await guild.system_channel.send(msg)

def setup(bot):
    bot.add_cog(EventCog(bot))

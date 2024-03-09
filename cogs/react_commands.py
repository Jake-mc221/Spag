import discord
from discord import Member
from discord.ext import commands
import random

# funnyi emoji related commands
class react_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.clown_user = None
        self.clown_amount = 5

    @commands.command()
    async def ratio(self, ctx, member: discord.Member):
        emojis = ctx.guild.emojis
        emojis = list(emojis)

        random.shuffle(emojis)

        async for message in ctx.channel.history(limit=200):
            if message.author == member:
                for e in emojis:
                    await message.add_reaction(e)
                return

    @commands.command()
    async def clown(self, ctx, member: discord.Member):
        self.clown_user = member
        self.clown_amount = 5

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author) == str(self.clown_user) and self.clown_amount > 0:
            self.clown_amount -= 1
            await message.add_reaction("🤡")

    @commands.command()
    async def flipcoin(self, ctx):
        """
        Flip a coin and react with either 👍 or 👎.
        """
        result = random.choice(["👍", "👎"])
        await ctx.send(result)

    @commands.command()
    async def roll(self, ctx):
        sides = 6
        result = random.randint(1, sides)
        await ctx.send(f"🎲 You rolled a {result}!")


async def setup(bot):
    await bot.add_cog(react_commands(bot))

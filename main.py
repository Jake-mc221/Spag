import asyncio
import os
from PIL import Image as PILImage

import discord
from discord.ext import commands
from cogs import ai_text
from helpers import key_helper


TOKEN = key_helper.read_key_from_file("keys.txt", "Discord")
INTENTS = discord.Intents.all()
ACT = discord.Game(name=ai_text.get_ai_res("hi",2.0))
bot = commands.Bot(command_prefix="!", intents=INTENTS, activity=ACT, help_command=None)
bot.per_rate = 2

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def test(ctx):
    await ctx.send("test")

@bot.command()
async def help(ctx):
    msg = """
Spag Commands List
    Image commands
        -!pfp
        -!fast
        -!swirl
        -!blur
        -!deepfry
        -!implode
        -!oilpaint
        -!meme
        -!dis
    React commands
        -!ratio
        -!clown
    AI commands
        -!setrate
        -!gen
        -!talk
    Misc commands
        -!download
        -!anon
        -!porn
        -!status
        -!big
        -!rev
        -!greentext
        -!settemp
        -!roll
        -!abort
        -!selfdestruct 
        
    Music commands
        -!play
    """
    await ctx.send(f'```css\n{msg}\n```')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')




async def main():
    await load()
    await bot.start(TOKEN)






asyncio.run(main())

import time
import random
from discord.ext import commands
import discord
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import faces
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import yt_dlp as youtube_dl


# contains a bunch of wip commands, most kind suck atm
class misc_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx, *, arg):
        await self.bot.change_presence(activity=discord.Game(name=arg))

    @commands.command()
    async def porn(self, ctx, *, arg):
        url = "https://www.redgifs.com/gifs/" + arg
        print(url)
        await self.get_random_gif_from_webpage(url,arg,ctx)

    # so far kinda works, issues with sound
    async def get_random_gif_from_webpage(self, url: str, arg, ctx):
        print("test")

        # Setup Selenium WebDriver
        service = Service(ChromeDriverManager().install())

        options = Options()
        options.add_argument('--headless')
        browser = webdriver.Chrome(service=service, options=options)

        browser.get(url)

        last_height = browser.execute_script("return document.body.scrollHeight")
        i = 0
        while i < 3:
            # Scroll down to the bottom
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            i += 1

        # Get the HTML content after JavaScript execution
        html = browser.page_source
        browser.quit()
        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        gif_elements = soup.select('a.title, a.isVideo')
        #print(gif_elements)

        if gif_elements:
            # Randomly select an element
            random_element = random.choice(gif_elements)
            # Extract the href attribute
            href = random_element.get('href')
            href = href.replace("watch", "ifr")
            print(href)
            arg = "/" + arg
            url = url.replace(str(arg), "")
            url = url.replace("/gifs", "")
            url = url + href

            await self.download(ctx,url)

    # download a video from youtube, works well but kinda messy
    @commands.command()
    async def download(self, ctx, url):
        # Download video using youtube-dl
        print(url)
        ydl_opts = {
            'format': 'worst',
            'outtmpl': 'video.%(ext)s',
            'force_overwrites': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Ensure the final file is in mp4 format
            }, {
                'key': 'FFmpegMerger',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(e)

        # Send video file to Discord channel
        try:
            # Attempt to send the file
            await ctx.send(file=discord.File('video.mp4'))
        except Exception as e:
            # If sending fails, print an error message
            print(f"An error occurred while sending the file: {e}")
            await ctx.send(f"`An error occurred while sending the file: {e}`")
            await ctx.send("`Please try again`")
        finally:
            # Remove the file whether sending was successful or not
            if os.path.exists("video.mp4"):
                os.remove("video.mp4")

    # test command to talk through the bet
    @commands.command()
    async def anon(self, ctx, *, arg):
        channel = 240771274719232000
        target_channel = self.bot.get_channel(channel)

        await target_channel.send(arg)


async def setup(bot):
    await bot.add_cog(misc_commands(bot))

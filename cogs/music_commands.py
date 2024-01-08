import asyncio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL

# play youtube videos through the bot, not finished yet
class music_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # change to dict when multiple guilds, guild_name, url etc
        self.music_queues = []
        print(f"Initializing cog with bot: {bot}")

    @commands.command(pass_context=True)
    async def play(self, ctx, url):
        if not self.music_queues:
            self.music_queues.append("blue_tooth.mp3")

        self.music_queues.append(url)

        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        print(voice)
        print(channel)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            print("hello")
            await channel.connect()

        await self.play_all_songs(ctx)

    async def play_all_songs(self, ctx):

        for url in self.music_queues:
            await ctx.send('video title')
            await self.play_song(url, ctx)

        self.music_queues = []

#   no need to pass ctx, fix this with dict
    async def play_song(self, url, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        # find better sol
        if 'youtube' in url:
            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            url = info['url']

        voice.play(FFmpegPCMAudio(
            executable=r"C:\Users\jake.mcandrew\Desktop\ffmpeg-2023-11-28-git-47e214245b-full_build\bin\ffmpeg.exe",
            source=url))

        while voice.is_playing():
            await asyncio.sleep(1)



async def setup(bot):
    await bot.add_cog(music_commands(bot))

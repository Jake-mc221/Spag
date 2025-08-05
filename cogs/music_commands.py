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


        try:
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                await channel.connect()
        except Exception as e:
            print(f"Error connecting: {e}")
            await ctx.send("Failed to connect to the voice channel.")
            return

        await self.play_all_songs(ctx)

    async def play_all_songs(self, ctx):
        for url in self.music_queues:
            await self.play_song(url, ctx)

        self.music_queues = []

#   no need to pass ctx, fix this with dict
    async def play_song(self, url, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        try:
            # find better sol
            if 'youtube' in url:
                YDL_OPTIONS = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'quiet': True,
                    'extract_flat': False,
                    'default_search': 'auto'
                }

                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                url = info['url']

            voice.play(FFmpegPCMAudio(
                executable=r"C:\Users\Server\Desktop\ffmpeg-7.1.1-full_build\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe",
                source=url))

            while voice.is_playing():
                await asyncio.sleep(1)
        except Exception as e:
            print(e)

    @commands.command()
    async def stop(self, ctx):
        """Stops the music and clears the queue."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            if voice.is_playing():
                voice.stop()
            await voice.disconnect()

        self.music_queues = []
        self.now_playing = None
        await ctx.send("Stopped the music and cleared the queue.")

    @commands.command()
    async def skip(self, ctx):
        """Skips the currently playing song."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            self.skip_flag = True
            voice.stop()
            await ctx.send("Skipped the song.")
        else:
            await ctx.send("No song is currently playing.")


async def setup(bot):
    await bot.add_cog(music_commands(bot))

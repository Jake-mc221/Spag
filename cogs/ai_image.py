import discord
from discord.ext import commands
import requests
import io
from PIL import Image
from helpers import key_helper
TOKEN = key_helper.read_key_from_file("keys.txt", "Huggingface")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HEADERS = {"Authorization": TOKEN}

API_URL2 = "https://api-inference.huggingface.co/models/suno/bark-small"
headers2 = {"Authorization": TOKEN}

API_URL3 = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# redo
class ai_images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gen(self, ctx, *, arg):
        payload = ({"inputs": arg,
                    "parameters": {"wait_for_model": True}})
        response = requests.post(API_URL3, headers=HEADERS, json=payload)
        print(response)
        print(arg)

        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        jpeg_img = image.convert("RGB")


        with io.BytesIO() as image_binary:
            jpeg_img.save(image_binary, 'JPEG')
            # Seek to the start of the BytesIO object
            image_binary.seek(0)
            # Send the JPEG image to the Discord channel
            await ctx.channel.send(file=discord.File(fp=image_binary, filename="image.jpeg"))

    @commands.command()
    async def talk(self, ctx, *, arg):
        payload = ({"inputs": arg})
        response = requests.post(API_URL2, headers=headers2, json=payload)
        audio_bytes = response.content

        print(response)

        filename = 'response.mp3'
        with open(filename, 'wb') as audio_file:
            audio_file.write(audio_bytes)

        # Send the file in Discord
        await ctx.send(file=discord.File(filename))


async def setup(bot):
    await bot.add_cog(ai_images(bot))

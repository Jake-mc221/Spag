from discord.ext import commands
from wand.image import Image
import requests
from io import BytesIO
import discord
from img_strategy.strat import Strategy, handler

class image_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.strat = Strategy
        self.handler = handler

    @commands.command()
    async def pfp(self, ctx, member: discord.Member = None):
        # If no member is specified, use the author of the message
        if member is None:
            member = ctx.author

        # Get the member's avatar URL
        avatar_url = member.avatar.url
        response = requests.get(avatar_url)

        avatar_bytes = BytesIO(response.content)

        # Send the avatar URL in the chat
        await ctx.send(file=discord.File(fp=avatar_bytes, filename='avatar.jpg'))

    @commands.command()
    async def blur(self, ctx, arg):
        print(arg)
        self.strat = self.handler.handle("blur")
        await self.process_image(ctx)


    @commands.command()
    async def swirl(self, ctx):
        self.strat = self.handler.handle("swirl")
        await self.process_image(ctx)

    @commands.command()
    async def sheer(self, ctx):
        self.strat = self.handler.handle("sheer")
        await self.process_image(ctx)

    @commands.command()
    async def implode(self, ctx):
        self.strat = self.handler.handle("implode")
        await self.process_image(ctx)

    async def process_image(self, ctx):
        message = ctx.message

        if message.reference and message.reference.resolved:
            message = message.reference.resolved

        print(len(message.attachments))
        if len(message.attachments) == 1:
            for attachment in message.attachments:
                try:
                    attachment = message.attachments[0]
                    response = requests.get(attachment.url)

                    with BytesIO(response.content) as input_buffer:
                        with Image(file=input_buffer) as img:
                            # Apply radial blur effect
                            img = self.strat.algo(img)

                            # Save the edited image to a buffer
                            output_buffer = BytesIO()
                            img.save(file=output_buffer)
                            output_buffer.seek(0)

                            # Send the image from the buffer
                            await ctx.channel.send(file=discord.File(output_buffer, filename='blurred_image.jpg'))


                except Exception as e:
                    print(e)
        else:
            await ctx.send("Error: Please upload only one image at a time.(multi images coming)")


async def setup(bot):
    await bot.add_cog(image_commands(bot))

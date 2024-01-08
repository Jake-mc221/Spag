from discord.ext import commands
from wand.image import Image
import requests
from io import BytesIO
import discord
from collections import namedtuple
from wand.color import Color

# all image related commands are temporary, funcs use the same copy and pasted code
# will be fixed in the future
class image_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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
    async def blur(self, ctx):
        message = ctx.message

        if message.reference and message.reference.resolved:
            message = message.reference.resolved

        # very yucky
        if len(message.attachments) == 1:
            for attachment in message.attachments:
                try:
                    attachment = message.attachments[0]
                    response = requests.get(attachment.url)

                    with BytesIO(response.content) as input_buffer:
                        with Image(file=input_buffer) as img:
                            # Apply radial blur effect
                            img.rotational_blur(angle = 10)

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

    @commands.command()
    async def swirl(self, ctx):
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
                            img.swirl(degree=-90)

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

    @commands.command()
    async def deepfry(self, ctx):
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
                            img.posterize(50, "floyd_steinberg")

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

    @commands.command()
    async def sheer(self, ctx):
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
                            img.shear('Red', 20, 30)

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

    @commands.command()
    async def implode(self, ctx):
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
                            img.implode(amount=0.35)

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

    @commands.command()
    async def t(self, ctx):
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
                            Point = namedtuple('Point', ['x', 'y', 'i', 'j'])

                            img.resize(140, 92)
                            img.background_color = Color('skyblue')
                            img.virtual_pixel = 'background'
                            img.artifacts['distort:viewport'] = "160x112-10+10"
                            img.artifacts['shepards:power'] = "4.0"
                            alpha = Point(0, 0, 30, 15)
                            beta = Point(70, 46, 60, 70)
                            args = (
                                *alpha,
                                *beta
                            )
                            img.distort('shepards', args)

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
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
    async def ascii(self, ctx):
        # Replace this with your ASCII art
        try:
            # Example ASCII art of a smiley face
            ascii_art = """
                                         8888  8888888
                  888888888888888888888888
               8888:::8888888888888888888888888
             8888::::::8888888888888888888888888888
            88::::::::888:::8888888888888888888888888
          88888888::::8:::::::::::88888888888888888888
        888 8::888888::::::::::::::::::88888888888   888
           88::::88888888::::m::::::::::88888888888    8
         888888888888888888:M:::::::::::8888888888888
        88888888888888888888::::::::::::M88888888888888
        8888888888888888888888:::::::::M8888888888888888
         8888888888888888888888:::::::M888888888888888888
        8888888888888888::88888::::::M88888888888888888888
      88888888888888888:::88888:::::M888888888888888   8888
     88888888888888888:::88888::::M::;o*M*o;888888888    88
    88888888888888888:::8888:::::M:::::::::::88888888    8
   88888888888888888::::88::::::M:;:::::::::::888888888
  8888888888888888888:::8::::::M::aAa::::::::M8888888888       8
  88   8888888888::88::::8::::M:::::::::::::888888888888888 8888
 88  88888888888:::8:::::::::M::::::::::;::88:88888888888888888
 8  8888888888888:::::::::::M::"@@@@@@"::::8w8888888888888888
  88888888888:888::::::::::M:::::"@a@":::::M8i8888888888888888
 8888888888::::88:::::::::M88:::::::::::::M88z88888888888888888
8888888888:::::8:::::::::M88888:::::::::MM888!888888888888888888
888888888:::::8:::::::::M8888888MAmmmAMVMM888*88888888   88888888
888888 M:::::::::::::::M888888888:::::::MM88888888888888   8888888
8888   M::::::::::::::M88888888888::::::MM888888888888888    88888
 888   M:::::::::::::M8888888888888M:::::mM888888888888888    8888
  888  M::::::::::::M8888:888888888888::::m::Mm88888 888888   8888
   88  M::::::::::::8888:88888888888888888::::::Mm8   88888   888
   88  M::::::::::8888M::88888::888888888888:::::::Mm88888    88
   8   MM::::::::8888M:::8888:::::888888888888::::::::Mm8     4
       8M:::::::8888M:::::888:::::::88:::8888888::::::::Mm    2
      88MM:::::8888M:::::::88::::::::8:::::888888:::M:::::M
     8888M:::::888MM::::::::8:::::::::::M::::8888::::M::::M
    88888M:::::88:M::::::::::8:::::::::::M:::8888::::::M::M
   88 888MM:::888:M:::::::::::::::::::::::M:8888:::::::::M:
   8 88888M:::88::M:::::::::::::::::::::::MM:88::::::::::::M
     88888M:::88::M::::::::::*88*::::::::::M:88::::::::::::::M
    888888M:::88::M:::::::::88@@88:::::::::M::88::::::::::::::M
    888888MM::88::MM::::::::88@@88:::::::::M:::8::::::::::::::*8
    88888  M:::8::MM:::::::::*88*::::::::::M:::::::::::::::::88@@
    8888   MM::::::MM:::::::::::::::::::::MM:::::::::::::::::88@@
     888    M:::::::MM:::::::::::::::::::MM::M::::::::::::::::*8
     888    MM:::::::MMM::::::::::::::::MM:::MM:::::::::::::::M
      88     M::::::::MMMM:::::::::::MMMM:::::MM::::::::::::MM
       88    MM:::::::::MMMMMMMMMMMMMMM::::::::MMM::::::::MMM
        88    MM::::::::::::MMMMMMM::::::::::::::MMMMMMMMMM
         88   8MM::::::::::::::::::::::::::::::::::MMMMMM
          8   88MM::::::::::::::::::::::M:::M::::::::MM
          
                
                
                
                
               """

            print("Sending ASCII art...")
            await ctx.send(f'```\n{ascii_art}\n```')
            print("ASCII art sent successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")



    @commands.command()
    async def fast(self, ctx):
        self.strat = self.handler.handle("fast")
        await self.process_image(ctx)

    @commands.command()
    async def blur(self, ctx):
        self.strat = self.handler.handle("blur")
        await self.process_image(ctx)

    @commands.command()
    async def swirl(self, ctx):
        self.strat = self.handler.handle("swirl")
        await self.process_image(ctx)

    @commands.command()
    async def deepfry(self, ctx):
        self.strat = self.handler.handle("deepfry")
        await self.process_image(ctx)

    @commands.command()
    async def sheer(self, ctx):
        self.strat = self.handler.handle("sheer")
        await self.process_image(ctx)

    @commands.command()
    async def implode(self, ctx):
        self.strat = self.handler.handle("implode")
        await self.process_image(ctx)

    @commands.command()
    async def oilpaint(self, ctx):
        self.strat = self.handler.handle("oilpaint")
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
                            img = self.strat.algo(img)

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

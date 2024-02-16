import random
from discord.ext import commands
from transformers import AutoModelForCausalLM, AutoTokenizer
from happytransformer import HappyGeneration
from happytransformer import GENSettings

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("xHexyy/test3")
happy_gen = HappyGeneration("GPT2", "DarwinAnim8or/GPT-Greentext-355m")
args_top_k = GENSettings(no_repeat_ngram_size=3, do_sample=True, top_k=80, temperature=1.0, max_length=150,
                         early_stopping=False)


# static method, used to get response from the model
def get_ai_res(msg, temp):
    print(temp)
    response = ""
    # If the response is empty, the loop will continue and generate a new response
    while len(response.strip()) < 1:
        # Generate a response from the model
        # def tmep is 2.0
        new_user_input_ids = tokenizer.encode(tokenizer.eos_token + msg, return_tensors='pt')
        chat_history_ids = model.generate(new_user_input_ids,
                                          max_length=50,
                                          pad_token_id=tokenizer.eos_token_id,
                                          no_repeat_ngram_size=3,
                                          do_sample=True,
                                          top_k=100,
                                          top_p=3.0,
                                          temperature=temp)

        # Decode the response
        response = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Print the model's response
    print("Context: {}\nSpag: {}\n".format(msg, response))
    return response


# only responds if users says "spag"
class ai_text(commands.Cog):
    def __init__(self, bot):
        self.response_chance = 1.0
        self.bot = bot
        self.temp = 2.0
        print(f"Initializing cog with bot: {bot}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "spag" in str(message.content).lower():
            response = get_ai_res(str(message.content.replace("spag", "")), self.temp)

            await message.channel.send(response.strip())

    # sets the response rate for the bot
    @commands.command()
    async def setrate(self, ctx, *, arg):

        try:
            self.response_chance = float(arg)
            await ctx.channel.send(f"`Rate set to {self.response_chance}`")

        except ValueError:
            await ctx.channel.send("`Invalid input. Please enter a valid integer.`")

    # should prolly use a template for these 2 commands
    @commands.command()
    async def settemp(self, ctx, *, arg):
        try:
            self.temp = float(arg)
            await ctx.channel.send(f"`Temp set to {self.temp}`")

        except ValueError:
            await ctx.channel.send("`Invalid input. Please enter a valid integer.`")

    # static code will be fixed in the future
    # responds to a message unreported
    @commands.Cog.listener('on_message')
    async def on_message_two(self, message):
        random_number = random.randint(0, 99)
        vent_id = 750198744485462078

        if (self.response_chance > random_number
                and message.author != self.bot.user
                and message.channel.id != vent_id):
            response = get_ai_res("", self.temp)
            await message.channel.send(response.strip())

    @commands.Cog.listener('on_message')
    async def on_message_three(self, message):
        if self.bot.user.mentioned_in(message):
            await message.channel.send(get_ai_res(message.content))

    @commands.command()
    async def greentext(self, ctx, *args):
        string = ' '.join(args)
        if not string:
            string = ">be me"
        else:
            string = ">" + string

        result = happy_gen.generate_text(string, args=args_top_k)
        file = result.text.replace(r'\n', '').strip()

        for x in file:
            if x == ">":
                string += "\n"
            string += x

        await ctx.send(string)


async def setup(bot):
    await bot.add_cog(ai_text(bot))

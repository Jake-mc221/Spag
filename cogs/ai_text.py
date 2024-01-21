from discord.ext import commands
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("xHexyy/test3")


# static method, used to get response from the model
def get_ai_res(msg):
    response = ""
    # If the response is empty, the loop will continue and generate a new response
    while len(response.strip()) < 1:
        # Generate a response from the model
        new_user_input_ids = tokenizer.encode(tokenizer.eos_token + msg, return_tensors='pt')
        chat_history_ids = model.generate(new_user_input_ids,
                                          max_length=50,
                                          pad_token_id=tokenizer.eos_token_id,
                                          no_repeat_ngram_size=3,
                                          do_sample=True,
                                          top_k=100,
                                          top_p=3.0,
                                          temperature=2.0)

        # Decode the response
        response = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Print the model's response
    print("Context: {}\nSpag: {}\n".format(msg, response))
    return response

# only responds if users says "spag"
class ai_text(commands.Cog):
    def __init__(self, bot):
        self.response_chance = 1
        self.bot = bot
        print(f"Initializing cog with bot: {bot}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if "spag" in str(message.content).lower():
            response = get_ai_res(str(message.content.replace("spag", "")))
            await message.channel.send(response.strip())





async def setup(bot):
    await bot.add_cog(ai_text(bot))
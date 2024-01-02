import discord
from discord.ext import commands
from openai import OpenAI


class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.info = "目前沒有情境"

    def add(self, item):
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)
        self.buffer.append(item)

    def get_all(self):
        return self.buffer
    
    def query(self, command):
        message = [{
            "role" : "system",
            "content" : "依照對話給出的設定回應，以下是對話情境\n" + self.info
        }]

        for i in self.buffer:
            message.append({
                "role" : "system",
                "content" : i
            })

        message.append({
            "role" : "user",
            "content" : command
        })
        
        return message

    def clear(self):
        self.buffer.clear()


# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.buffer = Buffer(5)
        self.api_key = ""
    
    async def send(self, command, ctx):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=1.0,
            max_tokens=1024,
            messages=self.buffer.query(command=command)
        )
        print(response)
        price = response.usage.prompt_tokens / 1000 * 0.0015 + \
        response.usage.completion_tokens / 1000 * 0.002    # output的錢

        await ctx.send("%" + response.choices[0].message.content + "\n\n" +  f"錢錢{price}丟水溝囉!")


    # 前綴指令
    @commands.command()
    async def buffer(self, ctx: commands.Context):
        await ctx.send(self.buffer.get_all())
    
    # shut down
    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        await ctx.bot.logout()
        print("shut")
    
    @commands.command()
    async def clear(self, ctx: commands.Context):
        self.buffer.clear()

    @commands.command()
    async def test(self, ctx: commands.Context):
        await self.send(command="給一個對話建議", ctx=ctx)
    
    @commands.command()
    async def reply(self, ctx: commands.Context):
        await self.send(command="對我們的對話情境給三個對話建議", ctx=ctx)
    
    @commands.command()
    async def how(self, ctx: commands.Context):
        await self.send(command="評價我們對話品質", ctx=ctx)

    @commands.command()
    async def 臨一洪(self, ctx: commands.Context):
        await ctx.send("%" + "我很抱歉我是個拉基被刺仔，只會他媽的打雀魂")

    @commands.command()
    async def setup(self, ctx: commands.Context):
        self.buffer.clear()

        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=1024,
            temperature=1.0,
            messages=[{
                "role" : "user",
                "content" : "我想要練習如何搭訕陌生女孩。 你隨機提供一個搭訕場景後，由我發起對話。 往後的對話中，我將扮演搭訕你的男孩，請你扮演被我搭訕的女孩。已知條件：兩人都是18～24歲間的台灣人。女孩有著普遍台灣女生的性格。請只給出對話的人事時地物就好了，盡量減短，不需要對話內容"
            }]
        )
        self.buffer.info = response.choices[0].message.content

        price = response.usage.prompt_tokens / 1000 * 0.0015 + \
        response.usage.completion_tokens / 1000 * 0.002    # output的錢
        await ctx.send("%" + response.choices[0].message.content + "\n\n" +  f"錢錢{price}丟水溝囉!")


    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content.startswith(self.bot.command_prefix):
            return

        self.buffer.add(message.content)
        print(self.buffer.get_all())

        if message.author == self.bot.user:
            return
        
        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=1.0,
            max_tokens=128,
            messages=self.buffer.query(command="(回復一句就好)")
        )
        print(response)
        price = response.usage.prompt_tokens / 1000 * 0.0015 + \
        response.usage.completion_tokens / 1000 * 0.002    # output的錢

        await message.channel.send(response.choices[0].message.content)
        #await self.send(command="接續話題", ctx=ctx)



# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
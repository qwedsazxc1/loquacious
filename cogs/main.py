import discord
from discord.ext import commands

class Buffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []

    def add(self, item):
        if len(self.buffer) >= self.size:
            self.buffer.pop(0)
        self.buffer.append(item)

    def get_all(self):
        return self.buffer

    def clear(self):
        self.buffer.clear()


# 定義名為 Main 的 Cog
class Main(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.buffer = Buffer(10)

    # 前綴指令
    @commands.command()
    async def buffer(self, ctx: commands.Context):
        await ctx.send(self.buffer.get_all())

    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        self.buffer.add(message.content)

# Cog 載入 Bot 中
async def setup(bot: commands.Bot):
    await bot.add_cog(Main(bot))
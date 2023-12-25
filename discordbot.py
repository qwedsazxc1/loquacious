import discord
from dotenv import load_dotenv
import os

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


load_dotenv()  # 加载 .env 文件
bot_token = os.getenv('BOT_TOKEN')
# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

buffer = Buffer(3)

@client.event
async def on_ready():
    print(f"name --> {client.user}")


@client.event
async def on_message(message):
    global buffer
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return
    
    if message.content[0] == '!':
        if "!buffer" in message.content:
            await message.channel.send(buffer.get_all())
            #buffer.clear()
        else:
            await message.channel.send(message.content)
    else:
        buffer.add(message.content)

client.run(bot_token)

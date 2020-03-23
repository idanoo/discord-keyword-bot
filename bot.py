import discord
import os
import re
from dotenv import load_dotenv

# https://discordpy.readthedocs.io/en/latest/api.html

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.channel.id == int(os.getenv("SOURCE_CHANNEL")):
            if re.match(os.getenv("REGEX_MATCH"), message.content, re.IGNORECASE):
                chan_list = [x.strip() for x in os.getenv("DISCORD_CHANNELS").split(',')]
                for channel_id in chan_list:
                    channel = client.get_channel(int(channel_id))
                    await channel.send(message.content)

load_dotenv()
while True:
    try:
        client = MyClient()
        client.run(os.getenv("DISCORD_TOKEN"), bot=False)
    except:
        print("Error Occurred... retrying")


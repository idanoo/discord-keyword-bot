import discord
import os
import re
import time
from dotenv import load_dotenv

# https://discordpy.readthedocs.io/en/latest/api.html

class DiscordKeywordBot(discord.Client):
    CACHE_TTL = 900
    CACHE_DICT = {}
    CACHE_LAST_PURGE = 0

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.channel.id == int(os.getenv("SOURCE_CHANNEL")):
            if re.match(os.getenv("REGEX_MATCH"), message.content, re.IGNORECASE):
                DiscordKeywordBot.cache_purge()
                if DiscordKeywordBot.cache_check(message.content):
                    chan_list = [x.strip() for x in os.getenv("DISCORD_CHANNELS").split(',')]
                    for channel_id in chan_list:
                        channel = client.get_channel(int(channel_id))
                        await channel.send(message.content)

    def cache_check(msg):
        if msg in DiscordKeywordBot.CACHE_DICT:
            """ Has been sent before.. Check TTL """
            timestamp = DiscordKeywordBot.CACHE_DICT.get(msg)
            if timestamp <=(int(time.time()) + DiscordKeywordBot.CACHE_TTL):
                """ TTL Expired. """
                DiscordKeywordBot.CACHE_DICT[msg] = int(time.time())
                return True
            else:
                """ TTL Not Expired """
                return False
        else:
            DiscordKeywordBot.CACHE_DICT[msg] = int(time.time())
            return True

    def cache_purge():
        purge_timer = int(time.time()) - (DiscordKeywordBot.CACHE_TTL * 2)
        if DiscordKeywordBot.CACHE_LAST_PURGE <= purge_timer:
            print("Purging cache!!!")
            DiscordKeywordBot.CACHE_LAST_PURGE = int(time.time())
            """ Lets Purge!!! """
            for uniq_msg in DiscordKeywordBot.CACHE_DICT:
                if DiscordKeywordBot.CACHE_DICT.get(uniq_msg) <= purge_timer:
                    DiscordKeywordBot.CACHE_DICT.pop(msg, None)


load_dotenv()
while True:
    try:
        client = DiscordKeywordBot()
        client.run(os.getenv("DISCORD_TOKEN"), bot=False)
    except:
        print("Error Occurred... retrying")


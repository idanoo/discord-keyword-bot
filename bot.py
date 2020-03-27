import discord
import os
import re
import time
from dotenv import load_dotenv

# https://discordpy.readthedocs.io/en/latest/api.html

class DiscordKeywordBot(discord.Client):
    CACHE_TTL = 900
    CACHE_DICT = {}
    CACHE_NEXT_PURGE = int(time.time()) + 1800

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
                        await channel.send('test: ' + message.content)

    def cache_check(msg):
        if msg in DiscordKeywordBot.CACHE_DICT:
            """ Has been sent before.. Check TTL """
            if DiscordKeywordBot.CACHE_DICT.get(msg) <= int(time.time()):
                """ TTL Expired. """
                DiscordKeywordBot.CACHE_DICT[msg] = (int(time.time()) + DiscordKeywordBot.CACHE_TTL)
                return True
            else:
                """ TTL Not Expired """
                return False
        else:
            DiscordKeywordBot.CACHE_DICT[msg] = (int(time.time()) + DiscordKeywordBot.CACHE_TTL)
            return True

    def cache_purge():
        if DiscordKeywordBot.CACHE_NEXT_PURGE <= int(time.time()) :
            """ Lets Purge!!! """
            print("Total cache older than TTL*2. Purging old records.")
            DiscordKeywordBot.CACHE_NEXT_PURGE = (int(time.time()) + (DiscordKeywordBot.CACHE_TTL * 2))
            for uniq_msg in DiscordKeywordBot.CACHE_DICT:
                if DiscordKeywordBot.CACHE_DICT.get(uniq_msg) <= int(time.time()):
                    """ If TTL <= now, remove from cache """
                    DiscordKeywordBot.CACHE_DICT.pop(msg, None)


load_dotenv()
while True:
    try:
        client = DiscordKeywordBot()
        client.run(os.getenv("DISCORD_TOKEN"), bot=False)
    except:
        print("Error Occurred... retrying")


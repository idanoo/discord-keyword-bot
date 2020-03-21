# Python Discord Keyword Bot

A bot that listens to a channel for messages that matches a regex and posts to a set of other channels when it matches.

### Requirements
python3 / pip3

### Install
copy .env.example to .env and setup your user Token in .env  

    cp .env.example .env
    pip3 install -r requirements.txt
    # config .env as below
    python3 boy.py

### Config
.env file layout

    DISCORD_TOKEN="token_from_web"
    DISCORD_CHANNELS="channel_1_id,channel_2_id"
    SOURCE_CHANNEL="channel_id_to_listen_to"
    REGEX_MATCH="^.*(REGEX|TO|USE|TO|MATCH).*$"


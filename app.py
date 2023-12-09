import requests
import os

import discord
from discord.ext import commands

import modal

stub = modal.Stub(name="daily_memes",image=modal.Image.debian_slim().pip_install("discord.py", "requests"))

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready(secret=modal.Secret.from_name("daily-discord-memes")):
    print(f'Logged in as {client.user.name}')
    url = "https://memes-from-reddit.p.rapidapi.com/memes/top"
    querystring = {"limit":"3"}
    RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "memes-from-reddit.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    memes = [item['url'] for item in response.json()['data']]
    # Only GIFS and Images
    # memes = [item['url'] for item in response.json()['data'] if item.get('post_hint') == 'image']
    
    channel = client.get_channel(int(os.environ.get('CHANNEL_ID')))
    if channel is not None:
        for meme in memes:
            await channel.send(meme)

    await client.close()


@stub.function(secret=modal.Secret.from_name("daily-discord-memes"),schedule=modal.Period(days=1))
def run_bot():
    client.run(os.environ["DISCORD_BOT_TOKEN"])


@stub.local_entrypoint()
def main():
    run_bot.remote()
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

    REDDIT_CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
    REDDIT_CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
    REDDIT_USERNAME = os.environ["REDDIT_USERNAME"]
    REDDIT_PASSWORD = os.environ["REDDIT_PASSWORD"]

    client_auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    post_data = {"grant_type": "password", "username": REDDIT_USERNAME, "password": REDDIT_PASSWORD}
    headers = {"User-Agent": "DM by someguy"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    response.json()
    bearer_token = response.json()['access_token']

    url = "https://oauth.reddit.com//r/Animemes/top.json?limit=5"

    headers = {"Authorization": "bearer " + bearer_token, 
            "User-Agent": "DM by someguy"
            }
    response = requests.request("GET", url, headers=headers)

    print(response.text)
    response = response.json()
    response = response["data"]["children"]


    urls = [url["data"]["url_overridden_by_dest"] for url in response]
    
    channel = client.get_channel(int(os.environ.get('CHANNEL_ID')))
    if channel is not None:
        for url in urls:
            await channel.send(url)

    await client.close()


@stub.function(secret=modal.Secret.from_name("daily-discord-memes"),schedule=modal.Period(days=1))
def run_bot():
    client.run(os.environ["DISCORD_BOT_TOKEN"])


@stub.local_entrypoint()
def main():
    run_bot.remote()
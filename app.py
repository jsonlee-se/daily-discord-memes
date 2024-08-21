import requests
import os

import discord
from discord.ext import commands

import modal

app = modal.App(name="daily_memes",image=modal.Image.debian_slim().pip_install("discord.py", "requests"))

intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix="/", intents=intents)
subreddits = ["Dankmemes", "okbuddyretard", "Animemes", "clevercomebacks", "meirl", "dndmemes","facepalm"]

@client.event
async def on_ready(secret=modal.Secret.from_name("daily-discord-memes")):
    print(f'Logged in as {client.user.name}')
    CHANNEL_ID = int(os.environ["CHANNEL_ID"])
    
    for sub in subreddits:
        response = make_request(subreddit=sub)
        try:
            urls = [url["data"]["url_overridden_by_dest"] for url in response]
        except:
            print("Error getting url for subreddit: " + sub)
            continue
        channel = client.get_channel(CHANNEL_ID)
        if channel is not None:
            for url in urls:
                await channel.send(url)

    await client.close()

def make_request(subreddit, secret=modal.Secret.from_name("daily-discord-memes")):
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

    url = "https://oauth.reddit.com//r/" + subreddit + "/top.json?limit=1"

    headers = {"Authorization": "bearer " + bearer_token, 
            "User-Agent": "DM by someguy"
            }
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        try:
            response = response.json()
            return response["data"]["children"]
        except ValueError as e:
            print(e)
    else:
        print(response.status_code)
        print(response.text)
        return None

@app.function(secret=modal.Secret.from_name("daily-discord-memes"),schedule=modal.Period(days=1))
def run_bot():
    client.run(os.environ["DISCORD_BOT_TOKEN"])


@app.local_entrypoint()
def main():
    run_bot.remote()
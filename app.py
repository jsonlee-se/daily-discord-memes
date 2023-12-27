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
    url = "https://reddit.com/r/Animemes/top.json?limit=5"

    payload = ""
    headers = {
        "cookie": "loid=000000000qtint5b56.2.1703676395675.Z0FBQUFBQmxqQW5yQS1GdWRvUVlXY1hwVmpnRWd5Xzd2Mks2aDExQ3RKNWdHNzVNalN0N19QVXFQNFZUZnItX0pBSjBUTDFVUmJfdEJCcHFVVklNYW9Wbzl1clRtc3o5ZzRIYWdPTWY0YWtKUkg4QUU1c0c1eU1ZVWs5YWZhdzR1NnBLUkY5d1YtLXU; session_tracker=khqdoldbqjkrkljhkn.0.1703677799756.Z0FBQUFBQmxqQTluWW1VZ2RzOGtvRm5QREI5ZlZyX2V3R3BIejhESDlRVFZUbFJfQl9lb0RMb3BqSDZqa0R0TWR1SThrR21RYjBmT0YwZHJvbl9KQXprTVpiazNHckNmekF6QUtuR0ZSMHBqRUExSWRRcUs2RWNCLU5GdE1yRG5XaXozdkJXNnRScVQ; csv=2; edgebucket=rilTl3Kl7kkDkY70x0; csrf_token=3f6a3031090527eb1eeee4bed7e7fbf5; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJsb2lkIiwiZXhwIjoxNzAzNzYyODYwLjc5NjI1MSwiaWF0IjoxNzAzNjc2NDYwLjc5NjI1MSwianRpIjoiY2FkdFgtZWNsX3NiRzBBd3RickxnQUFpQmFoY01RIiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml9xdGludDViNTYiLCJsY2EiOjE3MDM2NzYzOTU2NzUsInNjcCI6ImVKeGtrZEdPdERBSWhkLWwxejdCX3lwX05odHNjWWFzTFFhb2szbjdEVm9jazcwN2NMNGlIUDhuS0lxRkxFMnVCS0drS1dFRld0T1VOaUx2NTh5OU9aRUZTeUZUUjg0M3l3b2thVXBQVW1ONXB5bFJ3V1prTGxmYXNVS0RCNllwVlM2WjIwS1BTNXZRM0kxRnowNk1xbHhXSHRUWW8zSnBiR01LMnhQanpjWnFReXF1eTZsTVlGa29uOFdMZnZ5Ry10WS1mN2JmaEhZd3JLZ0tEX1RPdUZ4d1lfSERGSGJfbnByMGJGMndxTDNYZzlRLTEtTjI3Yk5tb2RtNV9WelB2emFTY1RtRzVpZll2N3QtQ1IxNDVIbVpVUWN3WWcwX3lyQWo2X0N2T29ES0JRV01KWWhQSTVBcmwyX19KZGl1VGY4YXR5ZC0tR2JFVFdfNHJSbW81eExFb1VfajZ6Y0FBUF9fWERfZTR3IiwiZmxvIjoxfQ.FHMAVJNB9DtvJYfpW18K_0deGj9hF_WcuxuywV4T17Utg4DfgHHPLvL_c3YBSi505x3RyWogFZM5c0A2uAsZkwxOdbQA4z_Vby9Id5os1nqY1qhx1b4P7vi0xh2rZMEGyEDXbg_QrEw8OG6OsEvVNMO90K-a8ZJMKspV9J-floTCTQ0unMwLiITfiWsy693FDn3xn5Mr9zkBQ5x0HyOALCYbGhbfrB8AKqFwIB08p47FtUyeRdKgpYd3Ek7as8RIRParTF8vb2T9uprxcRHTp3irnNWOtZ88guM4RuSX3eCn_a6NHqr42h_HD_1rpR4GKSHZGg72WzkdbpXoBxOZxA",
        "User-Agent": "Insomnia/2023.5.7",
    }
    response = requests.request("GET", url, data=payload, headers=headers)

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
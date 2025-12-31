import praw
import requests

CLIENT_ID = 
CLIENT_SECRET = 
DISCORD_WEBHOOK_URL = 

subreddits = [
    "Dankmemes",
    "okbuddyretard",
    "Animemes",
    "clevercomebacks",
    "meirl",
    "dndmemes",
    "facepalm",
    "foundsatan",
    "pettyrevenge",
]
reddit = praw.Reddit(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = "DM by someguy"
)

if __name__ == "__main__":
    content = []
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).top(limit=1):
            content.append(submission.url)

        requests.post(DISCORD_WEBHOOK_URL, json={"content": "\n".join(content)})
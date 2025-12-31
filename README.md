# Daily Memes Discord Bot (AWS Lambda)

## Overview

This project is a **serverless Discord meme poster** written in Python and hosted on **AWS Lambda**.
It posts memes to Discord on a schedule using **Discord webhooks**, pulls content from Reddit via **PRAW**, and stores configuration and secrets using **AWS-native services**.

This is no longer a long-lived Discord bot process — it is a **stateless, scheduled job**, which makes it cheaper, simpler, and more reliable.

---

## Architecture

```
EventBridge (schedule)
        ↓
     AWS Lambda
        ↓
   Reddit API (via PRAW)
        ↓
   Discord Webhook
```

### AWS Services Used

* **AWS Lambda** — executes the meme posting job
* **EventBridge Scheduler** — triggers the Lambda on a schedule
* **AWS Secrets Manager** — stores API credentials and secrets
* **AWS SSM Parameter Store** — stores non-secret configuration (e.g. subreddit list)

---

## Features

* **Scheduled Meme Posting**
  Posts memes automatically based on an EventBridge schedule.

* **Reddit Integration via PRAW**
  Uses Reddit’s official Python API wrapper with OAuth (refresh token flow).

* **Discord Webhooks (No Bot Gateway)**
  Messages are sent via webhooks — no persistent Discord connection, no intents, no event loop.

* **Fully Serverless**
  No EC2 instances, no containers, no always-on processes.

---

## Requirements

* Python 3.9+ (I used 3.12)
* `praw`
* `requests`
* AWS account with access to:

  * Lambda
  * EventBridge
  * Secrets Manager
  * SSM Parameter Store

---

## Configuration

### Secrets (AWS Secrets Manager)

Stored as a single JSON secret:

```json
{
  "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/...",
  "REDDIT_CLIENT_ID": "...",
  "REDDIT_CLIENT_SECRET": "...",
  "REDDIT_REFRESH_TOKEN": "..."
}
```

These values are fetched at runtime by the Lambda function.

---

### Parameters (SSM Parameter Store)

Non-secret configuration is stored separately.

Example:

* `/daily-memes/subreddits` (Type: `StringList`)

Value:

```
Dankmemes,ProgrammerHumor,memes
```

This allows updating subreddit sources **without redeploying** the Lambda function.

---

## Discord Setup (Webhook-Based)

1. Open Discord channel settings
2. Create a webhook
3. Copy the webhook URL
4. Store it in **AWS Secrets Manager**

No Discord bot user or gateway connection is required.

---

## Reddit Setup

* Existing Reddit **script app** is used
* OAuth authorization is done once to obtain a **refresh token**
* The Lambda function uses the refresh token to request short-lived access tokens via PRAW

Username/password authentication is **not used**.

---

## Deployment

* Deploy the Lambda function with its IAM execution role
* Grant the role access to:

  * `secretsmanager:GetSecretValue`
  * `ssm:GetParameter`
* Configure an EventBridge schedule to invoke the function

---

## Why This Design

* **Lambda over long-lived bots**: avoids timeouts, gateway connections, and idle compute
* **Webhooks over discord.py**: simpler, faster, and more reliable for scheduled posting
* **SSM + Secrets Manager split**: clean separation of config vs credentials
* **PRAW over raw HTTP**: less OAuth pain, more stability

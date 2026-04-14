# Slack Greeting Bot – Slack Events API + Django

A Slack bot built with Django and the Slack Events API.  
The bot listens to events from Slack and responds when a user greets it.
The application runs a Django backend that receives events from Slack through the Events API.  
Since the backend runs locally during development, ngrok is used to expose the local server to the internet.

Users can:
* Mention the bot in a channel
* Send greeting messages
* Receive automated responses from the bot

## Requirements
* Python >= 3.11	
* Conda (creates a Virtual Environment with its own python, django and tools)
* Django (backend framework for Python, hosts an http server -similar to NestJS-)
* Slack Workspace
* ngrok
* Git
* Anaconda Prompt / CMD / Git Bash

## Tech Stack
### Backend
- Python v3.11
- Django (receives http requests from slack events)
- Django REST Framework (Django extension for managing API endpoints)
- Slack Python SDK (to engage with Slack API using Python)
- Slack Events API

### Infrastructure
- ngrok (for exposing our local server to Slack)

## Setup and Execution

1. Setup your project:
```
chmod -x setup.sh
./setup.sh
```

2. Run the application
```
chmod -x run.sh
./run.sh
```

3. Create an .env file following the .env_example. You'll need to create your own Slack App at https://api.slack.com/apps/; in Features → OAuth & Permissions → Scope, add bot token scopes for your bot to be able to write and read from the channels you add it to. In OAuth Tokens, click Install to <your Slack Project> to get the Authentication and Verification Tokens needed for the .env.

4. Log in to ngrok and create a domain to start a tunnel (you can reuse an existing ngrok domain if you already have one)

5. Use ngrok in a new terminal to expose your local server. From slackbot/ngrok run:
```
./ngrok http 8000 --url=<YOUR_NGROK_URL>
```

6. Copy the generated public URL and configure it in your Slack App:

Slack App → Event Subscriptions → Request URL → <YOUR_NGROK_URL>/events/

Example:
```
https://xxxx.ngrok.io/slack/events/
```

Make sure ngrok is running so Slack can reach your local backend.
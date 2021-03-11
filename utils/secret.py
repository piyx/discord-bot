import os
from dotenv import load_dotenv

load_dotenv('.env')  # Create a env file and set your secret variables in it

# Reddit secret
# Get it from https://www.reddit.com/prefs/apps/
CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Discord token
# Get it from https://discord.com/developers/applications
TOKEN = os.getenv("BOT_TOKEN")

# Weather api_key
# Get it from https://www.weatherapi.com/
WEATHER_API = os.getenv("WEATHER_API")

# Nasa api
# Get it from https://api.nasa.gov/
NASA_API = os.getenv("NASA_API")
print(TOKEN)

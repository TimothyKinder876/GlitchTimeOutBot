import requests
import os
from dotenv import load_dotenv

#This is not my code idk how it works

load_dotenv()
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')

def get_twitch_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data.get("access_token")


def is_streamer_live(username):
    if username == "":
        return
    token = get_twitch_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        "https://api.twitch.tv/helix/streams",
        headers=headers,
        params={"user_login": username}
    )
    # Basic error handling
    response.raise_for_status()
    data = response.json()
    
    # If streamer is live, return the stream data dict
    if data.get("data"):
        return data["data"][0]
    
    # Not live -> return None
    return None


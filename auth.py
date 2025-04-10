import os
from dotenv import load_dotenv, set_key
import urllib.parse
import requests

load_dotenv()

client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
redirect_uri = os.getenv("TWITCH_REDIRECT_URI")
scopes = "chat:read"
response_type = "code"

base_url = "https://id.twitch.tv/oauth2/authorize"
params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": response_type,
    "scope": scopes
}
oauth_url = f"{base_url}?{urllib.parse.urlencode(params)}"

print("Open this URL in your web browser to authorize your application:")
print(oauth_url)
print("-" * 30)

authorization_code = input("Enter the authorization code from the browser URL: ")
print("-" * 30)

if client_secret:
    token_url = "https://id.twitch.tv/oauth2/token"
    token_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }

    try:
        response = requests.post(token_url, params=token_params)
        response.raise_for_status()
        token_data = response.json()

        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")

        if access_token and refresh_token:
            # Save the access token and refresh token to the .env file
            set_key(".env", "TWITCH_ACCESS_TOKEN", access_token)
            set_key(".env", "TWITCH_REFRESH_TOKEN", refresh_token)
            print("Successfully obtained and saved access token and refresh token to .env")
            print("-" * 30)
            print("You can now run the chat monitor script.")
        else:
            print("Failed to obtain access token or refresh token.")
            print("Response:", token_data)

    except requests.exceptions.RequestException as e:
        print(f"Error during token exchange: {e}")
        if response is not None:
            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

else:
    print("Error: TWITCH_CLIENT_SECRET not found in environment variables.")
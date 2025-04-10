import asyncio
import websockets
import os
import random
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("TWITCH_ACCESS_TOKEN")
twitch_username = os.getenv("TWITCH_USERNAME")
channels_to_join_str = os.getenv("TWITCH_CHANNELS_TO_JOIN")  # Get the comma-separated string

if channels_to_join_str:
    channels_to_join = [channel.strip() for channel in channels_to_join_str.split(',')]
else:
    channels_to_join = ["xqc"]  # Default channel if TWITCH_CHANNELS is not set or empty

COLORS = [
    "\033[31m",  # Red
    "\033[32m",  # Green
    "\033[33m",  # Yellow
    "\033[34m",  # Blue
    "\033[35m",  # Magenta
    "\033[36m",  # Cyan
    "\033[91m",  # Bright Red
    "\033[92m",  # Bright Green
    "\033[93m",  # Bright Yellow
    "\033[94m",  # Bright Blue
    "\033[95m",  # Bright Magenta
    "\033[96m",  # Bright Cyan
]

RESET_COLOR = "\033[0m"
user_colors = {} 

async def get_user_color(username):
    """Assigns a random color to a username and stores it."""
    if username not in user_colors:
        user_colors[username] = random.choice(COLORS)
    return user_colors[username]

async def chat_monitor():
    uri = "wss://irc-ws.chat.twitch.tv:443"
    try:
        async with websockets.connect(uri) as websocket:
            if not access_token or not twitch_username:
                print("Error: TWITCH_ACCESS_TOKEN or TWITCH_USERNAME not found in environment variables.")
                return 
            await websocket.send(f"PASS oauth:{access_token}")
            await websocket.send(f"NICK {twitch_username.lower()}")
            await websocket.send("CAP REQ twitch.tv/commands twitch.tv/tags")
            for channel in channels_to_join:
                await websocket.send(f"JOIN #{channel.lower()}")
                print(f"Joined channel: {channel}")
            async for message in websocket:
                if message.startswith("PING"):
                    await websocket.send("PONG :tmi.twitch.tv")
                elif "PRIVMSG" in message:
                    try:
                        parts = message.split(" :", 1)
                        if len(parts) == 2:
                            metadata, message_content = parts
                            user_info_part = metadata.split(" ")[0]
                            channel = metadata.split(" ")[2]
                            username = user_info_part.split("!")[0][1:]
                            user_color = await get_user_color(username)
                            colored_username = f"{user_color}{username}{RESET_COLOR}"
                            print(f"[{channel}] {colored_username}: {message_content}", end='')  
                        else:
                            print(f"Unexpected PRIVMSG format: {message}") 
                    except IndexError:
                        print(f"Error parsing PRIVMSG: {message}") 
                    except Exception as e:
                        print(f"An unexpected error occurred during PRIVMSG parsing: {e}")
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(chat_monitor())
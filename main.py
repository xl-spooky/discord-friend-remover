from discord.ext import commands
import requests
import time
from typing import Any

start_time = time.time()
bot = commands.Bot(command_prefix='!s ', self_bot=True)

TOKEN: str = "YOUR_ACC_TOKEN"  # Replace this with your user token (Note: Using a user token is against Discord's TOS)
API_BASE_URL: str = "https://discord.com/api/v9"

headers: dict[str, str] = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# list of friend user IDs you do not want to delete (as integers), Leave empty if there are no friends to exclude as [].
DO_NOT_DELETE_IDS: list[int] = [
    404264989147529217,
    # Continue if there are more to exclude.
]

def get_friends() -> list[dict[str, Any]]:
    """Fetches the list of friends for the user account."""
    url: str = f"{API_BASE_URL}/users/@me/relationships"
    response: requests.Response = requests.get(url, headers=headers)
    if response.status_code == 200:
        friends: list[dict[str, Any]] = response.json()
        return [friend for friend in friends if friend['type'] == 1]  # Type 1 means "friend"
    else:
        print("Failed to get friends")
        return []

def remove_friend(user_id: int) -> None:
    """Removes a friend based on user ID."""
    url: str = f"{API_BASE_URL}/users/@me/relationships/{user_id}"
    response: requests.Response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Successfully removed friend {user_id}")
    else:
        print(f"Failed to remove friend {user_id}: {response.status_code}")

@bot.event
async def on_ready() -> None:
    if bot.user is not None:
        print(f'Logged in as {bot.user.name} ({bot.user.id})')
    else:
        print('Bot user is None, unable to retrieve name or ID.')

@bot.command()
async def remove(ctx: commands.Context) -> None:
    """Command to remove all friends from the user's friend list, except those in the do-not-delete list."""
    friends: list[dict[str, Any]] = get_friends()
    for friend in friends:
        # Convert friend ID to integer for comparison
        friend_id: int = int(friend['id'])
        
        if friend_id in DO_NOT_DELETE_IDS:
            print(f"Skipping friend: {friend['user']['username']}#{friend['user']['discriminator']} (ID: {friend_id})")
            continue

        try:
            print(f"Removing friend: {friend['user']['username']}#{friend['user']['discriminator']} (ID: {friend_id})")
            remove_friend(friend_id)
        except Exception as e:
            print(f"Couldn't remove: {friend['user']['username']}#{friend['user']['discriminator']} (ID: {friend_id}). Reason: {e}")

bot.run(TOKEN)

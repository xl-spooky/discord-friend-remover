from discord.ext import commands
from discord import Message, Member
import requests
import time
from typing import Any
import random
import asyncio
from art import text2art

start_time = time.time()
bot = commands.Bot(command_prefix='!s ', self_bot=True)

TOKEN: str = "USE_YOUR_TOKEN"  # Replace this with your user token (Note: Using a user token is against Discord's TOS)
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
    await ctx.message.delete()
    friends: list[dict[str, Any]] = get_friends()
    for friend in friends:
        friend_id: int = int(friend['id'])
        
        if friend_id in DO_NOT_DELETE_IDS:
            print(f"Skipping friend: {friend['user']['username']}#{friend['user']['discriminator']} (ID: {friend_id})")
            continue

        try:
            print(f"Removing friend: {friend['user']['username']}#{friend['user']['discriminator']} (ID: {friend_id})")
            remove_friend(friend_id)
        except Exception as e:
            print(f"Couldn't remove: {friend['user']['username']}#{friend['user']['discriminator']} (ID: {friend_id}). Reason: {e}")

@bot.command()
async def roll(ctx: commands.Context) -> None:
    """Rolls a six-sided dice."""
    await ctx.message.delete()
    dice_result = random.randint(1, 6)
    await ctx.send(f'🎲 You rolled a {dice_result}!')

@bot.command()
async def flip(ctx: commands.Context) -> None:
    """Flips a coin."""
    await ctx.message.delete()
    result = random.choice(['Heads', 'Tails'])
    await ctx.send(f'🪙 It\'s {result}!')

@bot.command(name='8ball')
async def eightball(ctx: commands.Context, *, question: str) -> None:
    """Answers a yes/no question."""
    await ctx.message.delete()
    responses = [
        "Yes", "No", "Maybe", "Definitely", "Absolutely not", "Ask again later", 
        "I'm not sure", "It is certain", "Very doubtful", "Without a doubt"
    ]
    answer = random.choice(responses)
    await ctx.send(f'🎱 {answer}')

@bot.command()
async def compliment(ctx: commands.Context) -> None:
    """Sends a random compliment."""
    await ctx.message.delete()
    compliments = [
        "You are like a ray of sunshine on a really dreary day.",
        "You are a smart cookie.",
        "Your positive energy is infectious.",
        "You are an awesome friend.",
        "You have a great sense of humor."
    ]
    compliment = random.choice(compliments)
    await ctx.send(f'😊 {compliment}')

@bot.command()
async def meme(ctx: commands.Context) -> None:
    """Sends a random meme."""
    await ctx.message.delete()
    meme_url = "https://meme-api.com/gimme"
    response = requests.get(meme_url)
    if response.status_code == 200:
        meme_data = response.json()
        meme_image = meme_data["url"]
        await ctx.send(meme_image)
    else:
        await ctx.send("Couldn't fetch a meme at the moment. Please try again later!")

@bot.command()
async def reverse(ctx: commands.Context, *, text: str) -> None:
    """Reverses the provided text."""
    await ctx.message.delete()
    reversed_text = text[::-1]
    await ctx.send(reversed_text)

@bot.command()
async def mock(ctx: commands.Context, *, text: str) -> None:
    """Converts text into a mocking spongebob meme format."""
    await ctx.message.delete()
    mocked_text = ''.join(random.choice([c.upper(), c.lower()]) for c in text)
    await ctx.send(mocked_text)

@bot.command()
async def ascii(ctx: commands.Context, *, text: str) -> None:
    """Converts text into ASCII art."""
    await ctx.message.delete()
    try:
        ascii_art = text2art(text)
        await ctx.send(f'```\n{ascii_art}\n```')
    except Exception as e:
        await ctx.send(f"Couldn't generate ASCII art. Error: {e}")

@bot.command()
async def fact(ctx: commands.Context) -> None:
    """Sends a random fact."""
    await ctx.message.delete()
    facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Bananas are berries, but strawberries aren't.",
        "Octopuses have three hearts.",
        "A single strand of spaghetti is called a spaghetto.",
        "Cows have best friends and can become stressed when they are separated from them."
    ]
    fact = random.choice(facts)
    await ctx.send(f'📚 Did you know? {fact}')

@bot.command()
async def scramble(ctx: commands.Context) -> None:
    """Starts a word scramble game with a random word fetched from an API."""
    await ctx.message.delete()
    try:
        response = requests.get('https://random-word-api.herokuapp.com/word')
        response.raise_for_status()
        word: str = response.json()[0]
    except requests.RequestException:
        await ctx.send("❌ Failed to fetch a word. Please try again later.")
        return

    scrambled_word: str = ''.join(random.sample(word, len(word)))
    await ctx.send(f'🔀 Unscramble this word: **{scrambled_word}**')

    def check(m: Message) -> bool:
        """Check if the message is from the invoking user and in the same channel."""
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg: Message | None = await bot.wait_for('message', check=check, timeout=30)  # Wait for 30 seconds for a response
        if msg and msg.content.lower() == word.lower():
            await ctx.send('🎉 Correct! Well done!')
        else:
            await ctx.send(f'❌ Sorry, the correct word was **{word}**.')
    except asyncio.TimeoutError:
        await ctx.send(f'⏰ Time\'s up! The correct word was **{word}**.')

@bot.command()
async def insult(ctx: commands.Context, member: Member) -> None:
    """Sends a playful insult to the mentioned user."""
    await ctx.message.delete()
    insults = [
        "You're as useful as a screen door on a submarine.",
        "You're not stupid; you just have bad luck thinking.",
        "You have the right to remain silent because whatever you say will probably be stupid anyway.",
        "If I wanted to kill myself, I’d climb your ego and jump to your IQ.",
        "You're proof that even god makes mistakes sometimes."
    ]
    insult = random.choice(insults)
    await ctx.send(f'{member.mention}, {insult}')

@bot.command()
async def story(ctx: commands.Context) -> None:
    """Generates a random short story."""
    await ctx.message.delete()
    stories = [
        "Once upon a time, in a land far, far away, there lived a small dragon who loved to bake cakes. One day, it decided to bake a cake for the king, and it turned out to be the best cake ever!",
        "In a quiet village, a young girl found a magical book that could make anything she wrote come true. She wrote herself a new pair of shoes, and when they appeared, they danced all on their own!",
        "A brave knight set out on a journey to find the missing piece of the moon. After many adventures, he found it in the belly of a giant fish and returned it to the sky, earning him a place among the stars."
    ]
    story = random.choice(stories)
    await ctx.send(f'📖 {story}')

bot.run(TOKEN)

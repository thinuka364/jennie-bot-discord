import os
import re
import discord
from keep_alive import keep_alive

# === Start the keep-alive server ===
keep_alive()

# === Bot config ===
TOKEN = os.environ["DISCORD_TOKEN"]
OWNER_ID = 1401868112793698328
TARGET_USER_ID = 408785106942164992
TRIGGER_PHRASE = "please complete this within 10 minutes or it may result in a ban"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ZERO_WIDTH_CHARS = ['\u200B', '\u200C', '\u200D', '\uFEFF']

def normalize_text(text: str) -> str:
    if text is None:
        return ""
    text = re.sub(r'<@!?\d+>', ' ', text)
    text = re.sub(r'<:[^>]+>', ' ', text)
    text = re.sub(r'<a:[^>]+>', ' ', text)
    for ch in ZERO_WIDTH_CHARS:
        text = text.replace(ch, '')
    text = text.replace('*', ' ').replace('|', ' ')
    text = re.sub(r'[^0-9A-Za-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text

NORMALIZED_TRIGGER = normalize_text(TRIGGER_PHRASE)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Alert trigger
    if message.author.id == TARGET_USER_ID:
        normalized_message = normalize_text(message.content)
        if NORMALIZED_TRIGGER in normalized_message:
            owner = await client.fetch_user(OWNER_ID)
            await owner.send(
                f"⚡ Alert: {message.author} sent the trigger phrase in your server\n"
                f"Original message:\n{message.content}"
            )
    
    # Owner command: jennie available
    if message.author.id == OWNER_ID and message.content.lower().strip() == "jennie available":
        await message.channel.send("Yes, working hard")

client.run(TOKEN)

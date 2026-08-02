import discord
from collections import defaultdict
from datetime import timedelta
import time

# Store user messages
spam_messages = defaultdict(list)

# Store warnings
warnings = defaultdict(int)

# Settings
SPAM_LIMIT = 5
SPAM_TIME = 5


async def check_spam(bot, message):
    # Ignore bots
    if message.author.bot:
        return

    now = time.time()
    user_id = message.author.id

    # Save message time
    spam_messages[user_id].append(now)

    # Remove old messages
    spam_messages[user_id] = [
        t for t in spam_messages[user_id]
        if now - t <= SPAM_TIME
    ]

    # Not enough messages for spam
    if len(spam_messages[user_id]) < SPAM_LIMIT:
        return

    # Reset message counter
    spam_messages[user_id].clear()

    # Add warning
    warnings[user_id] += 1

    # Find logs channel
    logs = discord.utils.get(
        message.guild.text_channels,
        name="logs"
    )

    try:

        # First warning
        if warnings[user_id] == 1:

            await message.author.timeout(
                timedelta(minutes=5),
                reason="Spam"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} received a **5-minute timeout** for spamming.\n\n"
                f"📌 **First Warning**\n"
                f"Further spam will result in a **10-minute timeout**."
            )

            if logs:
                await logs.send(
                    f"🛡️ **Spam Det

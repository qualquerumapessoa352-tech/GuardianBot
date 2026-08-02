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

    # Check for spam
    if len(spam_messages[user_id]) < SPAM_LIMIT:
        return

    # Reset counter
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
                    f"🛡️ **Spam Detected**\n"
                    f"User: {message.author.mention}\n"
                    f"Punishment: 5-minute timeout"
                )

        # Second warning
        elif warnings[user_id] == 2:

            await message.author.timeout(
                timedelta(minutes=10),
                reason="Repeated Spam"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} received a **10-minute timeout** for spamming.\n\n"
                f"📌 **Second Warning**\n"
                f"🚨 Any further spam will result in an **automatic ban**."
            )

            if logs:
                await logs.send(
                    f"⚠️ **Second Warning**\n"
                    f"User: {message.author.mention}\n"
                    f"Punishment: 10-minute timeout"
                )

        # Third warning
        else:

            await message.guild.ban(
                message.author,
                reason="Repeated Spam"
            )

            await message.channel.send(
                f"🚨 {message.author.mention} has been **automatically banned** for repeated spam."
            )

            if logs:
                log = await logs.send(
                    f"🚨 **AUTOMATIC BAN**\n"
                    f"User: {message.author.mention}\n"
                    f"Reason: Repeated Spam"
                )

                await log.pin()

    except discord.Forbidden:
        print("Mimi doesn't have permission to punish this user.")

    except Exception as error:
        print(f"Anti-Spam Error: {error}")

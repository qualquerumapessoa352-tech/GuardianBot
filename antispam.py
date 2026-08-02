import discord
from collections import defaultdict
from datetime import timedelta
import time

from logs import send_log

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

    # Not enough messages yet
    if len(spam_messages[user_id]) < SPAM_LIMIT:
        return

    # Save spam messages
    spam_list = [message.content] * len(spam_messages[user_id])

    # Reset counter
    spam_messages[user_id].clear()

    # Add warning
    warnings[user_id] += 1

    try:

        # First Warning
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

            await send_log(
                guild=message.guild,
                title="🛡️ SPAM DETECTED",
                color=discord.Color.yellow(),
                user=message.author,
                channel=message.channel,
                punishment="5-minute Timeout",
                reason="Spam (5 messages in 5 seconds)",
                messages=spam_list
            )

        # Second Warning
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

            await send_log(
                guild=message.guild,
                title="⚠️ SECOND WARNING",
                color=discord.Color.orange(),
                user=message.author,
                channel=message.channel,
                punishment="10-minute Timeout",
                reason="Repeated Spam",
                messages=spam_list
            )

        # Third Warning
        else:

            await message.guild.ban(
                message.author,
                reason="Repeated Spam"
            )

            await message.channel.send(
                f"🚨 {message.author.mention} has been **automatically banned** for repeated spam."
            )

            await send_log(
                guild=message.guild,
                title="🚨 AUTOMATIC BAN",
                color=discord.Color.red(),
                user=message.author,
                channel=message.channel,
                punishment="Automatic Ban",
                reason="Repeated Spam",
                messages=spam_list,
                pin=True
            )

    except discord.Forbidden:
        print("Mimi doesn't have permission to punish this user.")

    except Exception as error:
        print(f"Anti-Spam Error: {error}")

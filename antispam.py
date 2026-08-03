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
import discord
from collections import defaultdict
from datetime import timedelta
import time

from logs import log_timeout, log_ban

# Store user messages
spam_messages = defaultdict(list)

# Store warnings
warnings = defaultdict(int)

# Settings
SPAM_LIMIT = 5
SPAM_TIME = 5


async def check_spam(bot, message):

    if message.author.bot:
        return

    now = time.time()
    user_id = message.author.id

    spam_messages[user_id].append(now)

    spam_messages[user_id] = [
        t for t in spam_messages[user_id]
        if now - t <= SPAM_TIME
    ]

    if len(spam_messages[user_id]) < SPAM_LIMIT:
        return

    spam_messages[user_id].clear()

    warnings[user_id] += 1

    try:

        # FIRST WARNING
        if warnings[user_id] == 1:

            await message.author.timeout(
                timedelta(minutes=5),
                reason="Spam"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} received a **5-minute timeout** for spamming.\n\n"
                f"📌 First Warning\n"
                f"Further spam will result in a **10-minute timeout**."
            )

            await log_timeout(
                guild=message.guild,
                user=message.author,
                channel=message.channel,
                duration="5 minutes",
                reason="Spam",
                message=message.content
            )

        # SECOND WARNING
        elif warnings[user_id] == 2:

            await message.author.timeout(
                timedelta(minutes=10),
                reason="Repeated Spam"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} received a **10-minute timeout** for spamming.\n\n"
                f"📌 Second Warning\n"
                f"🚨 Any further spam will result in an **automatic ban**."
            )

            await log_timeout(
                guild=message.guild,
                user=message.author,
                channel=message.channel,
                duration="10 minutes",
                reason="Repeated Spam",
                message=message.content
            )

        # THIRD WARNING
        else:

            await message.guild.ban(
                message.author,
                reason="Repeated Spam"
            )

            await message.channel.send(
                f"🚨 {message.author.mention} has been **automatically banned** for repeated spam."
            )

            await log_ban(
                guild=message.guild,
                user=message.author,
                channel=message.channel,
                reason="Repeated Spam",
                moderator="🤖 Mimi Security"
            )

    except discord.Forbidden:
        print("Mimi doesn't have permission to punish this user.")

    except Exception as error:
        print(f"Anti-Spam Error: {error}")

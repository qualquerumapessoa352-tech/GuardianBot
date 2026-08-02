import discord
from collections import defaultdict
from datetime import timedelta
import time

# Guarda mensagens e infrações
spam_messages = defaultdict(list)
warnings = defaultdict(int)

# Configurações
SPAM_LIMIT = 5      # 5 mensagens
SPAM_TIME = 5       # em 5 segundos


async def check_spam(bot, message):

    # Ignora bots
    if message.author.bot:
        return

    now = time.time()
    user_id = message.author.id

    # Guarda o horário da mensagem
    spam_messages[user_id].append(now)

    # Remove mensagens antigas
    spam_messages[user_id] = [
        t for t in spam_messages[user_id]
        if now - t <= SPAM_TIME
    ]

    # Se atingiu o limite
    if len(spam_messages[user_id]) >= SPAM_LIMIT:

        warnings[user_id] += 1

        # Canal de logs
        logs = discord.utils.get(
            message.guild.text_channels,
            name="logs"
        )

        # 1ª infração
        if warnings[user_id] == 1:

            await message.author.timeout(
                timedelta(minutes=5),
                reason="Spam"
            )

            await message.channel.send(
                f"🛡️ **Anti-Spam | Mimi**\n"
                f"{message.author.mention} recebeu um **timeout de 5 minutos** por spam.\n"
                f"⚠️ Esta é a **1.ª infração**."
            )

            try:
                await message.author

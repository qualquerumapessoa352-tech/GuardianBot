import discord
from collections import defaultdict
from datetime import timedelta
import time


# Guarda as mensagens dos utilizadores
spam_messages = defaultdict(list)

# Guarda o nível de infração
warnings = defaultdict(int)


# Configuração
SPAM_LIMIT = 5
SPAM_TIME = 5


async def check_spam(bot, message):

    # Ignora bots
    if message.author.bot:
        return

    user_id = message.author.id
    now = time.time()

    # Guarda o horário da mensagem
    spam_messages[user_id].append(now)

    # Remove mensagens antigas
    spam_messages[user_id] = [
        t for t in spam_messages[user_id]
        if now - t <= SPAM_TIME
    ]


    # Detectou spam
    if len(spam_messages[user_id]) >= SPAM_LIMIT:

        warnings[user_id] += 1

        print(
            f"Spam detectado: {message.author}"
        )


        if warnings[user_id] == 1:

            await message.author.timeout(
                timedelta(minutes=5),
                reason="Spam"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} recebeu timeout de 5 minutos por spam."
            )


        elif warnings[user_id] == 2:

            await message.author.timeout(
                timedelta(minutes=10),
                reason="Spam repetido"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} recebeu timeout de 10 minutos."
            )


        else:

            await message.guild.ban(
                message.author,
                reason="Spam repetido"
            )

            await message.channel.send(
                f"🚨 {message.author.mention} foi banido por spam."
            )


        # limpa depois da punição
        spam_messages[user_id].clear()

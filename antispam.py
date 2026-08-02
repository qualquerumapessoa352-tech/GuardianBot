import discord
from collections import defaultdict
from datetime import timedelta
import time

# Guarda as mensagens de cada utilizador
spam_messages = defaultdict(list)

# Guarda o número de infrações
warnings = defaultdict(int)

# Configurações
SPAM_LIMIT = 5
SPAM_TIME = 5


async def check_spam(bot, message):
    # Ignora bots
    if message.author.bot:
        return

    now = time.time()
    user_id = message.author.id

    # Guarda o momento da mensagem
    spam_messages[user_id].append(now)

    # Remove mensagens antigas
    spam_messages[user_id] = [
        t for t in spam_messages[user_id]
        if now - t <= SPAM_TIME
    ]

    # Verifica spam
    if len(spam_messages[user_id]) < SPAM_LIMIT:
        return

    # Limpa a lista para não repetir imediatamente
    spam_messages[user_id].clear()

    warnings[user_id] += 1

    # Procura o canal "logs"
    logs = discord.utils.get(message.guild.text_channels, name="logs")

    try:
        if warnings[user_id] == 1:
            await message.author.timeout(
                timedelta(minutes=5),
                reason="Spam"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} recebeu um **timeout de 5 minutos** por spam."
            )

            if logs:
                await logs.send(
                    f"🛡️ {message.author} recebeu timeout de 5 minutos por spam."
                )

        elif warnings[user_id] == 2:
            await message.author.timeout(
                timedelta(minutes=10),
                reason="Spam repetido"
            )

            await message.channel.send(
                f"⚠️ {message.author.mention} recebeu um **timeout de 10 minutos** por spam."
            )

            if logs:
                await logs.send(
                    f"⚠️ {message.author} recebeu timeout de 10 minutos."
                )

        else:
            await message.guild.ban(
                message.author,
                reason="Spam repetido"
            )

            await message.channel.send(
                f"🚨 {message.author.mention} foi **banido automaticamente** por spam."
            )

            if logs:
                log = await logs.send(
                    f"🚨 **BAN AUTOMÁTICO**\nUtilizador: {message.author}"
                )
                await log.pin()

    except discord.Forbidden:
        print("O Mimi não tem permissão para aplicar a punição.")

    except Exception as erro:
        print(f"Erro no Anti-Spam: {erro}")

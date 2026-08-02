import discord
from discord.ext import commands
from collections import defaultdict
from datetime import timedelta
import time

# Guarda infrações e mensagens
spam_messages = defaultdict(list)
warnings = defaultdict(int)

# Configurações
SPAM_LIMIT = 5       # 5 mensagens
SPAM_TIME = 5        # em 5 segundos


async def check_spam(bot, message):
    if message.author.bot:
        return

    now = time.time()
    user_id = message.author.id

    spam_messages[user_id].append(now)

    # Remove mensagens antigas
    spam_messages[user_id] = [
        t for t in spam_messages[user_id]
        if now - t <= SPAM_TIME
    ]

    # Detectou spam
    if len(spam_messages[user_id]) >= SPAM_LIMIT:

        warnings[user_id] += 1

        # Procura o canal de logs
        logs = discord.utils.get(
            message.guild.text_channels,
            name="logs"
        )

        if warnings[user_id] == 1:
            await message.author.timeout(
                timedelta(minutes=5),
                reason="Spam"
            )

            try:
                await message.author.send(
                    "⚠️ Recebeste um timeout de **5 minutos** por spam.\n"
                    "Esta é a tua **1.ª advertência**."
                )
            except:
                pass

            if logs:
                await logs.send(
                    f"🛡️ **Spam Detectado**\n"
                    f"Utilizador: {message.author.mention}\n"
                    f"Mensagem:\n```{message.content}```\n"
                    f"Punição: Timeout 5 minutos"
                )

        elif warnings[user_id] == 2:

            await message.author.timeout(
                timedelta(minutes=10),
                reason="Spam"
            )

            try:
                await message.author.send(
                    "⚠️ Timeout de **10 minutos**.\n"
                    "Na próxima infração serás banido."
                )
            except:
                pass

            if logs:
                await logs.send(
                    f"⚠️ Segunda infração\n"
                    f"{message.author.mention}\n"
                    f"```{message.content}```"
                )

        else:

            await message.guild.ban(
                message.author,
                reason="Spam Repetido"
            )

            if logs:
                msg = await logs.send(
                    f"🚨 **BAN AUTOMÁTICO**\n"
                    f"Utilizador: {message.author.mention}\n"
                    f"Mensagem:\n```{message.content}```"
                )

                await msg.pin()

            try:
                await message.author.send(
                    "🚫 Foste banido por spam repetido.\n"
                    "Se achares que foi um erro, fala com a Owner."
                )
            except:
                pass

        spam_messages[user_id].clear()

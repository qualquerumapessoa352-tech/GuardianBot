import discord
from discord.ext import commands
import os

from antispam import check_spam
from logs import log_message_delete, log_message_edit, log_ban


intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"{bot.user} está online!")
    print("VERSÃO NOVA DO MIMI LIGADA")

    await bot.change_presence(
        activity=discord.Game(
            name="🛡️ Protegendo o servidor"
        )
    )


@bot.event
async def on_message(message):

    await check_spam(bot, message)

    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    await log_message_delete(message)


@bot.event
async def on_message_edit(before, after):
    await log_message_edit(before, after)


@bot.event
async def on_member_ban(guild, user):
    await log_ban(
        guild,
        user,
        None,
        "Banimento automático",
        "🤖 Mimi Security"
    )


TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)

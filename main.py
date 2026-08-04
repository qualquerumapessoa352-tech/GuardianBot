import discord
from discord.ext import commands
import os

from antispam import check_spam
from antilinks import check_links

from logs import (
    log_message_delete,
    log_message_edit,
    log_ban,
    log_channel_delete,
    log_channel_create,
    log_channel_update
)

from tickets import setup as setup_tickets


intents = discord.Intents.all()


class MimiBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        # Carrega o sistema de suporte
        await self.load_extension("support")


bot = MimiBot()


@bot.event
async def on_ready():
    print(f"{bot.user} está online!")
    print("VERSÃO NOVA DO MIMI LIGADA")

    # Carrega sistema de tickets apenas uma vez
    if not hasattr(bot, "tickets_loaded"):
        await setup_tickets(bot)
        bot.tickets_loaded = True

    await bot.change_presence(
        activity=discord.Game(
            name="🛡️ Protegendo o servidor"
        )
    )


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    await check_spam(bot, message)
    await check_links(message)

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
        "🛡️ Mimi Security"
    )



@bot.event
async def on_guild_channel_delete(channel):
    await log_channel_delete(channel)



@bot.event
async def on_guild_channel_create(channel):
    await log_channel_create(channel)



@bot.event
async def on_guild_channel_update(before, after):
    await log_channel_update(before, after)



TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("ERRO: TOKEN não encontrado!")
else:
    bot.run(TOKEN)

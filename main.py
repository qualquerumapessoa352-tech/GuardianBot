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
from support import SupportView # Importamos apenas a View visual do menu

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"{bot.user} está online!")
    print("VERSÃO NOVA DO MIMI LIGADA")

    # Garante que os botões do suporte continuem funcionando após reinicializações
    bot.add_view(SupportView())

    if not hasattr(bot, "tickets_loaded"):
        await setup_tickets(bot)
        bot.tickets_loaded = True

    await bot.change_presence(
        activity=discord.Game(
            name="🛡️ Protegendo o servidor"
        )
    )

# --- COMANDO DO PAINEL DE SUPORTE NOVO ---
@bot.command(name="setup-support", aliases=["support", "suporte"])
@commands.has_permissions(administrator=True)
async def setup_support_cmd(ctx):
    embed = discord.Embed(
        title="✨ SUPPORT & HELP CENTER",
        description=(
            "Need to speak with our staff team or open a formal request?\n\n"
            "**Questions, Partnerships, Reports, or Purchases**\n"
            "Select the desired department below. A private ticket channel will be created exclusively to handle your request individually."
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="Support available 24/7 • Mimi Bot")
    
    view = SupportView()
    await ctx.send(embed=embed, view=view)

@bot.event
async def on_message(message):
    # Ignora mensagens de outros bots para não dar erro
    if message.author.bot:
        return

    await check_spam(bot, message)
    await check_links(message)

    # Processa os comandos (isso faz o !setup-support e o !ticket funcionarem)
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

bot.run(TOKEN)

import discord
from discord.ext import commands
import os
from antispam import check_spam

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"{bot.user} está online!")

    comandos = await bot.tree.sync()
    print(f"{len(comandos)} comandos sincronizados")

    await bot.change_presence(
        activity=discord.Game(
            name="🛡️ Protegendo o servidor"
        )
    )


@bot.event
async def on_message(message):
    await check_spam(bot, message)

    await bot.process_commands(message)


@bot.tree.command(
    name="ping",
    description="Mostra a latência do Mimi"
)
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"🏓 Pong!\nLatência: **{latency}ms**"
    )


TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)

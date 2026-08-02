import discord
from discord.ext import commands
import os
from antispam import check_spam

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} está online!")
    await bot.change_presence(
        activity=discord.Game(name="🛡️ Protegendo o servidor")
    )


@bot.event
async def on_message(message):
    await check_spam(bot, message)

    await bot.process_commands(message)


bot.run(os.getenv("TOKEN"))

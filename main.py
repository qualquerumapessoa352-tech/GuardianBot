import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} está online!")
    await bot.change_presence(
        activity=discord.Game(name="🛡️ Protegendo o servidor")
    )

bot.run(os.getenv("TOKEN"))

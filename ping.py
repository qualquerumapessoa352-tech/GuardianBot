import discord
from discord import app_commands


async def setup(bot):

    @bot.tree.command(
        name="ping",
        description="Mostra a latência do Mimi"
    )
    async def ping(interaction: discord.Interaction):

        latency = round(bot.latency * 1000)

        await interaction.response.send_message(
            f"🏓 Pong!\nLatência: **{latency}ms**"
        )

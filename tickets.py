import discord
from discord.ext import commands
import asyncio

TICKET_CATEGORY = "Tickets"


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🎫 Criar Ticket",
        style=discord.ButtonStyle.green,
        custom_id="create_ticket"
    )
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(
            guild.categories,
            name=TICKET_CATEGORY
        )

        if category is None:
            category = await guild.create_category(TICKET_CATEGORY)

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category
        )

        await channel.set_permissions(
            user,
            read_messages=True,
            send_messages=True
        )

        await channel.set_permissions(
            guild.default_role,
            read_messages=False
        )

        embed = discord.Embed(
            title="🎫 Ticket Criado",
            description="Explique o seu problema. A staff irá responder em breve.",
            color=discord.Color.purple()
        )

        await channel.send(
            embed=embed,
            view=CloseTicketView()
        )

        await interaction.response.send_message(
            f"✅ Ticket criado: {channel.mention}",
            ephemeral=True
        )


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🔒 Fechar Ticket",
        style=discord.ButtonStyle.red,
        custom_id="close_ticket"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(
            "🔒 Ticket fechado. Este canal será apagado em **24 horas**."
        )

        await asyncio.sleep(86400)

        await interaction.channel.delete()


async def setup(bot):

    @bot.command()
    async def ticket(ctx):

        embed = discord.Embed(
            title="🎫 Sistema de Tickets",
            description="Clique no botão para abrir um ticket.",
            color=discord.Color.purple()
        )

        await ctx.send(
            embed=embed,
            view=TicketView()
        )

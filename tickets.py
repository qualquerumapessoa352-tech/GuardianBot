import discord
from discord.ext import commands
import asyncio

TICKET_CATEGORY = "Tickets"


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🎫 Create Ticket",
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
            title="🎫 Ticket Created",
            description="Please explain your issue. Our staff will assist you shortly.",
            color=discord.Color.purple()
        )

        await channel.send(
            embed=embed,
            view=CloseTicketView()
        )

        await interaction.response.send_message(
            f"✅ Ticket created: {channel.mention}",
            ephemeral=True
        )


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🔒 Close Ticket",
        style=discord.ButtonStyle.red,
        custom_id="close_ticket"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(
            "🔒 Ticket closed. This channel will be deleted in **24 hours**."
        )

        await asyncio.sleep(86400)

        await interaction.channel.delete()


async def setup(bot):

    @bot.command()
    async def support(ctx):

        embed = discord.Embed(
            title="🛡️ SUPPORT CENTER",
            description=(
                "Need help from our staff?\n\n"
                "• Support\n"
                "• Reports\n"
                "• Partnerships\n"
                "• Purchases\n\n"
                "Click the button below to create a private support ticket."
            ),
            color=discord.Color.purple()
        )

        embed.set_footer(
            text="💜 Mimi Security"
        )

        await ctx.send(
            embed=embed,
            view=TicketView()
        )

    @bot.command()
    async def ticket(ctx):

        embed = discord.Embed(
            title="🎫 Ticket System",
            description="Click the button below to create a ticket.",
            color=discord.Color.purple()
        )

        await ctx.send(
            embed=embed,
            view=TicketView()
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

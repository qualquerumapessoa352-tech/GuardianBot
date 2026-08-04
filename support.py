import discord
from discord.ext import commands


class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Select the ideal department here...",
        emoji="➤",
        style=discord.ButtonStyle.secondary,
        custom_id="support_menu"
    )
    async def support_menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "⚙️ Menu coming soon...",
            ephemeral=True
        )


async def setup(bot):

    @bot.command()
    async def support(ctx):

        embed = discord.Embed(
            title="✨ SUPPORT CENTER",
            description=(
                "Need to contact our staff or open a formal request?\n\n"
                "**Support, Partnerships, Reports or Purchases**\n"
                "Select the desired department below. A private chat will be opened "
                "exclusively to handle your request individually."
            ),
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text="24/7 Support • Mimi Bot"
        )

        await ctx.send(
            embed=embed,
            view=SupportView()
        )

  class SupportSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="General Support",
                description="Problems or reports involving the staff.",
                emoji="🛡️",
                value="support"
            ),
            discord.SelectOption(
                label="Partnerships",
                description="Collaboration and partnership requests.",
                emoji="🤝",
                value="partnerships"
            ),
            discord.SelectOption(
                label="Recruitment / Staff",
                description="Apply to join our team.",
                emoji="👑",
                value="staff"
            )
        ]

        super().__init__(
            placeholder="Select the ideal department here...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="support_select"
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            f"✅ You selected: **{self.values[0]}**",
            ephemeral=True
        )


class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SupportSelect())

  class SupportSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="General Support",
                description="Problems or reports involving the staff.",
                emoji="🛡️",
                value="support"
            ),
            discord.SelectOption(
                label="Partnerships",
                description="Collaboration and partnership requests.",
                emoji="🤝",
                value="partnerships"
            ),
            discord.SelectOption(
                label="Recruitment / Staff",
                description="Apply to join our team.",
                emoji="👑",
                value="staff"
            )
        ]

        super().__init__(
            placeholder="Select the ideal department here...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="support_select"
        )

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        option = self.values[0]

        category = discord.utils.get(
            guild.categories,
            name="Support Tickets"
        )

        if category is None:
            category = await guild.create_category("Support Tickets")

        ticket_name = f"{option}-{user.name}".lower().replace(" ", "-")

        existing = discord.utils.get(
            category.text_channels,
            name=ticket_name
        )

        if existing:
            await interaction.response.send_message(
                f"❌ You already have an open **{option}** ticket: {existing.mention}",
                ephemeral=True
            )
            return

        channel = await guild.create_text_channel(
            name=ticket_name,
            category=category
        )

        await channel.set_permissions(
            guild.default_role,
            read_messages=False
        )

        await channel.set_permissions(
            user,
            read_messages=True,
            send_messages=True
        )

        embed = discord.Embed(
            title="🎫 Support Ticket",
            description=(
                f"Welcome {user.mention}!\n\n"
                f"**Department:** {option.replace('-', ' ').title()}\n\n"
                "Please explain your request.\n"
                "A staff member will assist you shortly."
            ),
            color=discord.Color.blurple()
        )

        embed.set_footer(text="💜 Mimi Security")

        await channel.send(embed=embed)

        await interaction.response.send_message(
            f"✅ Your ticket has been created: {channel.mention}",
            ephemeral=True
        )

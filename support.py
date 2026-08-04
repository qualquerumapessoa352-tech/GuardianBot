
import discord
from discord.ext import commands
from discord import app_commands

class SupportSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="General Support",
                description="Issues or management reports",
                value="ticket_general",
                emoji="🛡️"
            ),
            discord.SelectOption(
                label="Partnerships Department",
                description="Collaboration and partnership proposals",
                value="ticket_partnerships",
                emoji="🤝"
            ),
            discord.SelectOption(
                label="Recruitment / Staff",
                description="Apply to join our staff team",
                value="ticket_recruitment",
                emoji="👑"
            )
        ]
        super().__init__(
            placeholder="Select the ideal department here...",
            min_values=1,
            max_values=1,
            custom_id="mimi_support_select"
        )

    async def callback(self, interaction: discord.Interaction):
        category_name = "General Support"
        if self.values[0] == "ticket_partnerships":
            category_name = "Partnerships"
        elif self.values[0] == "ticket_recruitment":
            category_name = "Recruitment"

        guild = interaction.guild
        user = interaction.user
        channel_name = f"ticket-{user.name.lower()}"

        # Verifica se o usuário já tem um ticket aberto
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            return await interaction.response.send_message(
                f"You already have an open ticket channel: {existing_channel.mention}",
                ephemeral=True
            )

        # Configura as permissões do canal privado
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            overwrites=overwrites
        )

        ticket_embed = discord.Embed(
            title=f"🎫 Mimi Support — {category_name}",
            description=f"Hello {user.mention}, welcome! Please explain your issue or request below. A staff member will assist you shortly.",
            color=discord.Color.blue()
        )
        await ticket_channel.send(content=user.mention, embed=ticket_embed)

        await interaction.response.send_message(
            f"Your ticket channel has been created: {ticket_channel.mention}",
            ephemeral=True
        )

class SupportView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SupportSelect())

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setup-support")
    @commands.has_permissions(administrator=True)
    async def setup_support(self, ctx):
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

async def setup(bot):
    await bot.add_cog(SupportCog(bot))

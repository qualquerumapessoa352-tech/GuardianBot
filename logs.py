import discord
from datetime import datetime

# Mimi purple color
MIMI_COLOR = discord.Color.from_rgb(155, 89, 182)


def create_embed(title, user, channel):
    embed = discord.Embed(
        title=title,
        color=MIMI_COLOR,
        timestamp=datetime.now()
    )

    embed.set_author(
        name="🛡️ Mimi Security"
    )

    embed.set_thumbnail(
        url=user.display_avatar.url
    )

    embed.add_field(
        name="👤 User",
        value=user.mention,
        inline=False
    )

    embed.add_field(
        name="📝 Username",
        value=str(user),
        inline=True
    )

    embed.add_field(
        name="🆔 User ID",
        value=str(user.id),
        inline=True
    )

    embed.add_field(
        name="💬 Channel",
        value=channel.mention,
        inline=False
    )

    embed.add_field(
        name="📅 Date",
        value=datetime.now().strftime("%d/%m/%Y"),
        inline=True
    )

    embed.add_field(
        name="🕒 Time",
        value=datetime.now().strftime("%H:%M:%S"),
        inline=True
    )

    embed.set_footer(
        text="💜 Mimi Security • Protecting your community"
    )

    return embed


async def send_embed(guild, embed, pin=False):
    logs = discord.utils.get(
        guild.text_channels,
        name="logs"
    )

import discord
from datetime import datetime


async def send_log(
    guild,
    title,
    color,
    user,
    channel,
    punishment,
    reason,
    messages=None,
    pin=False
):
    # Procura o canal #logs
    logs = discord.utils.get(
        guild.text_channels,
        name="logs"
    )

    if logs is None:
        return

    embed = discord.Embed(
        title=title,
        color=color,
        timestamp=datetime.now()
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
        value=user.id,
        inline=True
    )

    embed.add_field(
        name="💬 Channel",
        value=channel.mention,
        inline=False
    )

    embed.add_field(
        name="⚖️ Punishment",
        value=punishment,
        inline=False
    )

    embed.add_field(
        name="📌 Reason",
        value=reason,
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

    if messages:

        text = ""

        for msg in messages:
            text += f"• {msg}\n"

        embed.add_field(
            name="📨 Spam Messages",
            value=text,
            inline=False
        )

    embed.set_footer(
        text="🛡️ Mimi Security"
    )

    sent = await logs.send(
        embed=embed
    )

    if pin:
        await sent.pin()

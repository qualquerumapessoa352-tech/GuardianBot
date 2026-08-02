import discord
from datetime import datetime

# ==========================
# CORES
# ==========================

DEFAULT_COLOR = discord.Color.from_rgb(155, 89, 182)
BAN_COLOR = discord.Color.red()

# ==========================
# CANAL DE LOGS
# ==========================

def get_logs_channel(guild):
    return discord.utils.get(guild.text_channels, name="logs")


# ==========================
# ENVIAR EMBED
# ==========================

async def send_log(guild, embed, pin=False):
    channel = get_logs_channel(guild)

    if channel is None:
        return

    msg = await channel.send(embed=embed)

    if pin:
        try:
            await msg.pin(reason="Automatic Ban Log")
        except:
            pass


# ==========================
# EMBED BASE
# ==========================

def create_embed(
    title,
    user,
    *,
    color=DEFAULT_COLOR,
    channel=None,
    reason=None,
    punishment=None,
    moderator=None
):

    embed = discord.Embed(
        title=title,
        color=color,
        timestamp=datetime.now()
    )

    embed.set_author(name="🛡️ Mimi Security")

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

    if channel:
        embed.add_field(
            name="💬 Channel",
            value=channel.mention,
            inline=False
        )

    if reason:
        embed.add_field(
            name="📄 Reason",
            value=reason,
            inline=False
        )

    if punishment:
        embed.add_field(
            name="⚖️ Punishment",
            value=punishment,
            inline=False
        )

    if moderator:
        embed.add_field(
            name="👮 Moderator",
            value=moderator,
            inline=False
        )

    embed.set_footer(
        text="💜 Mimi Security"
    )

    return embed

# ==========================
# WARNING
# ==========================

async def log_warning(
    guild,
    user,
    channel,
    reason,
    moderator="🤖 Mimi Security"
):

    embed = create_embed(
        title="⚠️ User Warned",
        user=user,
        channel=channel,
        reason=reason,
        punishment="Warning",
        moderator=moderator
    )

    await send_log(guild, embed)


# ==========================
# TIMEOUT
# ==========================

async def log_timeout(
    guild,
    user,
    channel,
    duration,
    reason,
    moderator="🤖 Mimi Security"
):

    embed = create_embed(
        title="⏳ User Timed Out",
        user=user,
        channel=channel,
        reason=reason,
        punishment=f"Timeout ({duration})",
        moderator=moderator
    )

    await send_log(guild, embed)

# =========================
# KICK
# =========================

async def log_kick(
    guild,
    user,
    channel,
    reason,
    moderator
):

    embed = create_embed(
        title="👢 User Kicked",
        user=user,
        channel=channel,
        reason=reason,
        punishment="Kick",
        moderator=moderator
    )

    await send_log(guild, embed)


# ==========================
# BAN
# ==========================

async def log_ban(
    guild,
    user,
    channel,
    reason,
    moderator
):

    embed = create_embed(
        title="🔨 User Banned",
        user=user,
        color=BAN_COLOR,
        channel=channel,
        reason=reason,
        punishment="Ban",
        moderator=moderator
    )

    await send_log(guild, embed, pin=True)
# ==========================
# MESSAGE DELETE
# ==========================

async def log_message_delete(message):

    if message.author.bot:
        return

    embed = create_embed(
        title="🗑️ Message Deleted",
        user=message.author,
        channel=message.channel,
        reason="Message deleted"
    )

    if message.content:
        embed.add_field(
            name="💬 Message",
            value=f"```{message.content[:1000]}```",
            inline=False
        )

    if message.attachments:
        files = "\n".join(file.url for file in message.attachments)

        embed.add_field(
            name="📎 Attachments",
            value=files,
            inline=False
        )

    await send_log(message.guild, embed)


# ==========================
# MESSAGE EDIT
# ==========================

async def log_message_edit(before, after):

    if before.author.bot:
        return

    if before.content == after.content:
        return

    embed = create_embed(
        title="✏️ Message Edited",
        user=before.author,
        channel=before.channel,
        reason="Message edited"
    )

    embed.add_field(
        name="📝 Before",
        value=f"```{before.content[:1000] or 'Empty'}```",
        inline=False
    )

    embed.add_field(
        name="📝 After",
        value=f"```{after.content[:1000] or 'Empty'}```",
        inline=False
    )

    embed.add_field(
        name="🔗 Jump",
        value=f"[Open Message]({after.jump_url})",
        inline=False
    )

    await send_log(before.guild, embed)
        

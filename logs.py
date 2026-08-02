import discord
from datetime import datetime

# ==========================
# COLORS
# ==========================

DEFAULT_COLOR = discord.Color.from_rgb(155, 89, 182)  # Purple
BAN_COLOR = discord.Color.red()

# ==========================
# LOG CHANNEL
# ==========================

def get_logs_channel(guild):
    return discord.utils.get(guild.text_channels, name="logs")


# ==========================
# SEND EMBED
# ==========================

async def send_log(guild, embed, pin=False):
    channel = get_logs_channel(guild)

    if channel is None:
        return

    message = await channel.send(embed=embed)

    if pin:
        try:
            await message.pin(reason="Automatic ban log")
        except:
            pass


# ==========================
# BASE EMBED
# ==========================

def create_embed(
    title,
    user,
    channel=None,
    *,
    color=DEFAULT_COLOR,
    reason=None,
    punishment=None,
    moderator=None,
    messages=None
):

    embed = discord.Embed(
        title=title,
        color=color,
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

    if channel is not None:
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

    if messages:

        text = ""

        for msg in messages:
            if len(text + msg + "\n") > 1000:
                break
            text += msg + "\n"

        if text == "":
            text = "No messages recorded."

        embed.add_field(
            name="💬 Messages",
            value=f"```{text}```",
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


# ==========================
# WARNING LOG
# ==========================

async def log_warning(
    guild,
    user,
    channel,
    reason,
    messages=None,
    moderator="🤖 Mimi Security"
):

    embed = create_embed(
        title="⚠️ User Warned",
        user=user,
        channel=channel,
        reason=reason,
        punishment="Warning",
        moderator=moderator,
        messages=messages
    )

    await send_log(guild, embed)


# ==========================
# TIMEOUT LOG
# ==========================

async def log_timeout(
    guild,
    user,
    channel,
    duration,
    reason,
    messages=None,
    moderator="🤖 Mimi Security"
):

    embed = create_embed(
        title="⏳ User Timed Out",
        user=user,
        channel=channel,
        reason=reason,
        punishment=f"Timeout ({duration})",
        moderator=moderator,
        messages=messages
    )

    await send_log(guild, embed)


# ==========================
# KICK LOG
# ==========================

async def log_kick(
    guild,
    user,
    channel,
    reason,
    moderator,
    messages=None
):

    embed = create_embed(
        title="👢 User Kicked",
        user=user,
        channel=channel,
        reason=reason,
        punishment="Kick",
        moderator=moderator,
        messages=messages
    )

    await send_log(guild, embed)


# ==========================
# BAN LOG
# ==========================

async def log_ban(
    guild,
    user,
    channel,
    reason,
    moderator,
    messages=None
):

    embed = create_embed(
        title="🔨 User Banned",
        user=user,
        channel=channel,
        color=BAN_COLOR,
        reason=reason,
        punishment="Ban",
        moderator=moderator,
        messages=messages
    )

    await send_log(
        guild,
        embed,
        pin=True
    )

# ==========================
# MESSAGE DELETE LOG
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
            name="💬 Deleted Message",
            value=f"```{message.content[:1000]}```",
            inline=False
        )

    if message.attachments:
        files = "\n".join(a.url for a in message.attachments)
        embed.add_field(
            name="📎 Attachments",
            value=files,
            inline=False
        )

    await send_log(message.guild, embed)


# ==========================
# MESSAGE EDIT LOG
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
        value=f"```{before.content[:900] or 'Empty'}```",
        inline=False
    )

    embed.add_field(
        name="📝 After",
        value=f"```{after.content[:900] or 'Empty'}```",
        inline=False
    )

    embed.add_field(
        name="🔗 Message",
        value=f"[Jump to Message]({after.jump_url})",
        inline=False
    )

    await send_log(before.guild, embed)


# ==========================
# MEMBER JOIN
# ==========================

async def log_member_join(member):

    embed = create_embed(
        title="📥 Member Joined",
        user=member,
        reason="Member joined the server"
    )

    await send_log(member.guild, embed)


# ==========================
# MEMBER LEAVE
# ==========================

async def log_member_leave(member):

    embed = create_embed(
        title="📤 Member Left",
        user=member,
        reason="Member left the server"
    )

    await send_log(member.guild, embed)

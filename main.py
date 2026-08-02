import discord
from discord.ext import commands
import os

from antispam import check_spam
from logs import log_message_delete, log_message_edit, log_ban

@bot.event
async def on_message_delete(message):
    await log_message_delete(message)


@bot.event
async def on_message_edit(before, after):
    await log_message_edit(before, after)


@bot.event
async def on_member_ban(guild, user):
    await log_ban(
        guild,
        user,
        None,
        "Banimento automático",
        "🤖 Mimi Security"
    )

import discord
import re

ALLOWED_LINKS = [
    "youtube.com",
    "youtu.be",
    "spotify.com",
    "open.spotify.com",
    "tiktok.com",
    "vm.tiktok.com",
    "instagram.com",
    "www.instagram.com"
]

LINK_REGEX = r"https?://[^\s]+|www\.[^\s]+"


async def check_links(message):

    if message.author.bot:
        return

    if message.guild is None:
        return

    links = re.findall(LINK_REGEX, message.content.lower())

    if not links:
        return

    for link in links:

        permitido = False

        for dominio in ALLOWED_LINKS:
            if dominio in link:
                permitido = True
                break

        if permitido:
            continue

        try:
            await message.delete()

            await message.channel.send(
                f"🚫 {message.author.mention}, esse link não é permitido neste servidor.",
                delete_after=5
            )

        except discord.Forbidden:
            pass

        break

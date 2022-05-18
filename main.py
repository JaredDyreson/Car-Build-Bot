"""Simple Discord bot that adds up all the components"""

import re
import typing
import os

import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

_regexes = [
    re.compile(r"\*\*([\w|\s]*)"),
    re.compile(r".*(https.*)"),
    re.compile(
        "|".join(
            [
                r"\$(\d*\.\d{1,2})",  # e.g., $.50, .50, $1.50, $.5, .5
                r"\$(\d+)",  # e.g., $500, $5, 500, 5
                r"\$(\d+\.?)",  # e.g., $5.
            ]
        )
    ),
]

components: typing.List[float] = []

bot = commands.Bot(command_prefix="$")


@bot.command()
async def calculate(ctx, *args):
    current_channel = discord.utils.get(bot.get_all_channels(), name="focus-st")
    messages = await current_channel.history(limit=200).flatten()

    for message in filter(lambda x: "QuesoGrande" in str(x.author), messages):
        if match := _regexes[2].findall(message.content):
            matches = [
                sub_element
                for element in match
                for sub_element in element
                if sub_element
            ]
            for element in matches:
                components.append(float(element))

    await ctx.send(f"Total cost for your build is: ${sum(components):0.2f}")


bot.run(TOKEN)


from discord.ext.commands import Cog, command, cooldown, BucketType
from discord import Embed
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    create_button,
    create_select,
    create_actionrow,
    create_select_option,
    wait_for_component,
)


import json

with open("config.json") as config_file:
    config = json.load(config_file)

from cogs.db import collection as db

import logging

log = logging.getLogger()


class Profile(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="profile",
        description="See your Blackjack profile.",
    )
    async def see_profile(self, ctx: SlashContext):
        profile = db.find({"_id": ctx.author.id})[0]
        log.debug(profile)

        description = f"""**{ctx.author.mention}'s profile:**
        \n**👛Coins:** {int(profile['Coins'])} | **✨EXP:** {profile['EXP']}"""

        embed = Embed(description=description, color=ctx.author.color)

        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))

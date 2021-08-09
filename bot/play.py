from discord.ext.commands import Cog, command, cooldown, BucketType

from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (
    create_button,
    create_select,
    create_actionrow,
    create_select_option,
    wait_for_component,
)
from game.blackjack import b

import json

with open("config.json") as config_file:
    config = json.load(config_file)

# TODO: Implement coin betting


class Play(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="play", description="Play some blackjack!", guild_ids=[702352937980133386]
    )
    async def play_blackjack(self, ctx: SlashContext):
        await b.play(ctx)


def setup(bot):
    bot.add_cog(Play(bot))

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
import game.blackjack as blackjack

import json

with open("config.json") as config_file:
    config = json.load(config_file)


class Play(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="play", description="Play some blackjack!", guild_ids=[702352937980133386]
    )
    async def play_blackjack(self, ctx):
        blackjack.Blackjack.play()


def setup(bot):
    bot.add_cog(Play(bot))

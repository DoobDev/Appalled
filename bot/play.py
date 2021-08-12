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
from discord_slash.utils.manage_commands import create_option
import logging

from game.blackjack import Blackjack as b
from db import collection as db

import json

log = logging.getLogger()

with open("config.json") as config_file:
    config = json.load(config_file)

# TODO Implement coin betting


class Play(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="play",
        description="Play some blackjack!",
        guild_ids=[702352937980133386],
        options=[
            create_option(
                name="bet",
                description="Put down how much you want to bet.",
                option_type=4,
                required=True,
            )
        ],
    )
    async def play_blackjack(self, ctx: SlashContext, bet: int):
        current_coins = db.find({"_id": ctx.author.id})[0]["EXP"]
        log.debug(current_coins)
        current_coins -= bet
        log.debug(current_coins)
        db.update_one({"_id": ctx.author.id}, {"$set": {"Coins": current_coins}})

        await b(self.bot).play(ctx, bet)


def setup(bot):
    bot.add_cog(Play(bot))

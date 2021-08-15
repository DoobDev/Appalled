from discord.ext.commands import Cog, cooldown, BucketType

from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
import logging

from cogs.game.blackjack import Blackjack as b
from cogs.db import collection as db

import json

log = logging.getLogger()

with open("config.json") as config_file:
    config = json.load(config_file)


class Play(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="play",
        description="Play some blackjack!",
        options=[
            create_option(
                name="bet",
                description="Put down how much you want to bet.",
                option_type=4,
                required=True,
            )
        ],
    )
    @cooldown(1, 2, BucketType.user)
    async def play_blackjack(self, ctx: SlashContext, bet: int):
        current_coins = int(db.find({"_id": ctx.author.id})[0]["Coins"])
        log.debug(current_coins)
        if bet > current_coins:
            await ctx.send("⚠ You can't bet more then you have.", hidden=True)
        elif bet <= 0:
            await ctx.send("⚠ You can't bet less then 0.", hidden=True)
        else:
            current_coins -= bet
            log.debug(current_coins)

            db.update_one({"_id": ctx.author.id}, {"$set": {"Coins": current_coins}})

            await b(self.bot, bet).play(ctx, bet)


def setup(bot):
    bot.add_cog(Play(bot))

import datetime
import os
import discord
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

from cogs.db import collection as db

import json

log = logging.getLogger()

with open("config.json") as config_file:
    config = json.load(config_file)

# TODO Add a way to redeem certain codes for coins


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="daily", description="Get a daily reward")
    async def daily_cmd(self, ctx: SlashContext):
        check_daily = db.find({"_id": ctx.author.id})[0]["DailyReward"]

        if check_daily:
            daily_job = self.bot.daily_job

            await ctx.send(
                f"⚠ You already got your daily reward\n⌚ Daily rewards reset at: {daily_job.next_run_time}",
                hidden=True,
            )
        else:
            current_coins = db.find({"_id": ctx.author.id})[0]["Coins"]
            more_coins = int(current_coins) + 250

            db.update_one({"_id": ctx.author.id}, {"$set": {"DailyReward": True}})
            db.update_one({"_id": ctx.author.id}, {"$set": {"Coins": more_coins}})
            await ctx.send(
                "👛 You have claimed your daily reward!\n(👛 +250 Coins)", hidden=True
            )

    @cog_ext.cog_slash(name="weekly", description="Get a weekly reward")
    async def weekly_cmd(self, ctx: SlashContext):
        check_weekly = db.find({"_id": ctx.author.id})[0]["WeeklyReward"]

        if check_weekly:
            weekly_job = self.bot.weekly_job
            await ctx.send(
                f"⚠ You already got your weekly reward\n⌚ Weekly rewards reset at: {weekly_job.next_run_time}",
                hidden=True,
            )

        else:
            current_coins = db.find({"_id": ctx.author.id})[0]["Coins"]
            more_coins = int(current_coins) + 1000

            db.update_one({"_id": ctx.author.id}, {"$set": {"WeeklyReward": True}})
            db.update_one({"_id": ctx.author.id}, {"$set": {"Coins": more_coins}})
            await ctx.send(
                "👛 You have claimed your weekly reward!\n(👛 +1000 Coins)", hidden=True
            )

    @cog_ext.cog_slash(
        name="setcoins",
        description="[OWNER ONLY] Command to set coins.",
        options=[
            create_option(
                name="amount",
                description="Amount of coins to set",
                option_type=4,
                required=True,
            ),
            create_option(
                name="user",
                description="The user to set the coins for",
                option_type=6,
                required=True,
            ),
        ],
    )
    async def setcoins_cmd(self, ctx: SlashContext, amount: int, user: discord.User):
        if ctx.author.id not in config["OwnerIDs"]:
            await ctx.send(
                "⚠ You are not the owner of this bot, you can't use this.", hidden=True
            )

        else:
            db.update_one({"_id": user.id}, {"$set": {"Coins": amount}})
            await ctx.send(f"👛 Set {user.mention}'s Coins to {amount}", hidden=True)

    # @cog_ext.cog_slash(name="redeem", description="Redeem a special code for some extra coins!", guild_ids=[702352937980133386], options=[create_option(name="code", description="The code you would like to redeem", option_type=3, required=True)])
    # async def redeem_cmd(self, ctx: SlashContext, code: str):
    #     pass


def setup(bot):
    bot.add_cog(Misc(bot))

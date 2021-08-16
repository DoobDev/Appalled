from discord.ext import commands
from discord_slash import SlashContext
from cogs.db import collection as db
import pymongo
import logging

log = logging.getLogger()


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command(self, ctx: SlashContext):
        try:
            db.find({"_id": ctx.author.id})[0]["EXP"]
        except IndexError:
            await ctx.send("⚠ Your user profile could not be found", hidden=True)
            db.insert_one(
                {
                    "_id": ctx.author.id,
                    "UserID": ctx.author.id,
                    "Coins": 100,
                    "EXP": 0,
                    "Level": 0,
                    "DailyReward": False,
                    "WeeklyReward": False,
                }
            )

            await ctx.send(
                "✅ Your user profile has been created! So try the command again!",
                hidden=True,
            )

        else:
            pass


def setup(bot):
    bot.add_cog(Events(bot))

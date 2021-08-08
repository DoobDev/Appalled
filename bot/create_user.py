from discord.ext import commands
from discord_slash import SlashContext
from db import collection as db
import pymongo


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command(self, ctx: SlashContext):
        try:
            db.insert_one(
                {
                    "_id": ctx.author.id,
                    "UserID": ctx.author.id,
                    "Coins": 100,
                    "EXP": 0,
                }
            )
        except pymongo.errors.DuplicateKeyError:
            pass


def setup(bot):
    bot.add_cog(Events(bot))

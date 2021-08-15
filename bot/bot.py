import discord
import os
import json
from glob import glob
import logging
from rich.logging import RichHandler

from discord.ext.commands import AutoShardedBot as Bot
from discord.ext.commands.errors import NoEntryPointError
from discord_slash import SlashCommand

from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from db import collection as db


load_dotenv()
# COGS = [path.split(os.sep)[-1][:-3] for path in glob("./cogs/*.py")]

with open("./config.json", "r") as config_file:
    config = json.load(config_file)

log_level = logging.DEBUG if config["dev_mode"] else logging.INFO
log = logging.getLogger()

logging.basicConfig(
    level=log_level,
    format="%(name)s - %(message)s",
    datefmt="%X",
    handlers=[RichHandler()],
)


class NoRunningFilter(logging.Filter):
    def filter(self, record):
        return not record.msg.startswith("Running job")


class NoRunningFilter2(logging.Filter):
    def filter(self, record):
        return not record.msg.startswith("Job")


running_job_filter = NoRunningFilter()
job_filter = NoRunningFilter2()
logging.getLogger("apscheduler.executors.default").addFilter(running_job_filter)
logging.getLogger("apscheduler.executors.default").addFilter(job_filter)


class Bot(Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = False
        intents.presences = False

        self.scheduler = AsyncIOScheduler()

        self.scheduler.add_job(self.reset_daily, CronTrigger(hour=0))
        self.scheduler.add_job(self.reset_weekly, CronTrigger(day=1))

        super().__init__(
            command_prefix="/",
            owner_ids=config["OwnerIDs"],
            intents=intents,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(everyone=False),
            help_command=None,
        )

        self.launch()

    async def reset_daily(self):
        db.update_many({"_id": {"$exists": True}}, {"$set": {"DailyReward": False}})
        log.debug("Daily Rewards reset")

    async def reset_weekly(self):
        db.update_many({"_id": {"$exists": True}}, {"$set": {"WeeklyReward": False}})
        log.debug("Weekly Rewards reset")

    def load_cogs(self):
        self.scheduler.start()
        self.load_extension("create_user")
        log.info("Loaded `create_user`")
        self.load_extension("play")
        log.info("Loaded `play`")
        self.load_extension("profile")
        log.info("Loaded `profile`")
        self.load_extension("misc")
        log.info("Loaded `misc`")

        # for cog in COGS:
        #     self.load_extension(f'{cog}')

    def launch(self):
        _ = SlashCommand(self, sync_commands=True, sync_on_cog_reload=True)
        self.load_cogs()

        log.info("Blackjack bot started!")
        self.run(os.environ.get("TOKEN"))

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="Blackjack | /play | Check Appalled's Discord user bio!"))

bot = Bot()

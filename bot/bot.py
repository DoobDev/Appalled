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

load_dotenv()
COGS = [path.split(os.sep)[-1][:-3] for path in glob("./cogs/*.py")]

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


        super().__init__(
            command_prefix="/",
            owner_ids=config["OwnerIDs"],
            intents=intents,
            case_insensitive=True,
        )

        self.launch()

    def load_cogs(self):
        self.load_extension("create_user")
        print("Loaded `create_user`")
        self.load_extension("play")
        print("Loaded `play`")

        # for cog in COGS:
        #     self.load_extension(f'{cog}')

    def launch(self):
        _ = SlashCommand(self, sync_commands=True, sync_on_cog_reload=True)
        self.load_cogs()

        print("Blackjack bot started!")
        self.run(os.environ.get("TOKEN"))


bot = Bot()

import discord
import os
import json
from glob import glob

from discord.ext.commands import AutoShardedBot as Bot
from discord.ext.commands.errors import NoEntryPointError
from discord_slash import SlashCommand

from dotenv import load_dotenv
load_dotenv()
COGS = [path.split(os.sep)[-1][:-3] for path in glob("./cogs/*.py")]

with open("./config.json", 'r') as config_file:
    config = json.load(config_file)

class Bot(Bot):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(
            command_prefix='/',
            owner_ids=config['OwnerIDs'],
            intents=intents,
            case_insensitive=True
        )

        self.launch()

    def load_cogs(self):
        self.load_extension('create_user')
        print("Loaded `create_user`")
        self.load_extension('play')
        print("Loaded `play`")

        # for cog in COGS:
        #     self.load_extension(f'{cog}')

    def launch(self):
        self.load_cogs()
        SlashCommand(self, sync_commands=True, sync_on_cog_reload=True)

        print("Blackjack bot started!")
        self.run(os.environ.get('TOKEN'))

bot = Bot()
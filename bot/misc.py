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

from db import collection as db

import json

log = logging.getLogger()

with open("config.json") as config_file:
    config = json.load(config_file)

# TODO Implement coin betting


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Misc(bot))

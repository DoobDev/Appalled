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
from game.blackjack import Blackjack as b

import json

with open("config.json") as config_file:
    config = json.load(config_file)

# TODO: Implement coin betting


class Play(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="play", description="Play some blackjack!", guild_ids=[702352937980133386]
    )
    async def play_blackjack(self, ctx: SlashContext):
        add = [1, 10, 15, 100, 150, 200]
        subtract = [-1, -10, -15, -100, -150, -200]

        add_buttons = [
            create_button(
                style=ButtonStyle.success,
                label=f"{button}",
                custom_id=f"addbet_{button}",
            )
            for button in add
        ]

        subtract_buttons = [
            create_button(
                style=ButtonStyle.danger,
                label=f"{button}",
                custom_id=f"subtractbet_{button}",
            )
            for button in subtract
        ]

        buttons = [create_actionrow(*add_buttons), create_actionrow(*subtract_buttons)]

        await ctx.send("Bet!", components=buttons, hidden=True)

        bet = 0
        while True:
            btn_ctx: ComponentContext = await wait_for_component(
                self.bot, components=buttons
            )
            btn_id = btn_ctx.component.custom_id

            bet_increase = int(str(btn_id).split("_")[-1])

        # await b(self.bot).play(ctx)


def setup(bot):
    bot.add_cog(Play(bot))

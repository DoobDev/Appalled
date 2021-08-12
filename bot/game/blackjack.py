# from models.deck import Deck
# from models.player import Player
import asyncio
import random
from discord_slash import cog_ext
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import (
    create_button,
    create_actionrow,
    wait_for_component,
)
from discord_slash.model import ButtonStyle

from db import collection as db

# TODO Add buttons for `Hit/Stand`
# TODO Make embeds.


class Card:
    def __init__(self, value, suit):
        self.cost = value
        self.value = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"][
            value - 1
        ]
        self.suit = "♠♥♦🍀"[suit]

    def price(self):
        if self.cost >= 10:
            return 10
        elif self.cost == 1:
            return 11
        return self.cost

    async def show(self, ctx):
        return self.suit, self.value


class Deck:
    def __init__(self):
        self.cards = []

    def generate(self):
        for i in range(1, 14):
            for j in range(4):
                self.cards.append(Card(i, j))

    def draw(self, iteration):
        cards = []
        for _ in range(iteration):
            card = random.choice(self.cards)
            self.cards.remove(card)
            cards.append(card)
        return cards

    def count(self):
        return len(self.cards)


class Player:
    def __init__(self, isDealer, deck):
        self.cards = []
        self.isDealer = isDealer
        self.deck = deck
        self.score = 0

    def check_score(self):
        a_counter = 0
        self.score = 0
        for card in self.cards:
            if card.price() == 11:
                a_counter += 1
            self.score += card.price()

        while a_counter != 0 and self.score > 21:
            a_counter -= 1
            self.score -= 10
        return self.score

    def hit(self):
        self.cards.extend(self.deck.draw(1))
        self.check_score()
        if self.score > 21:
            return 1

        return 0

    def deal(self):
        self.cards.extend(self.deck.draw(2))
        self.check_score()
        if self.score == 21:
            return 1
        return 0

    async def show(self, ctx):
        description = ""
        card_str = ""
        card_str = "**Dealer's hand:**\n" if self.isDealer else "**Your hand:**\n"
        for i in self.cards:
            suit, value = await i.show(ctx)
            description += f"\n{suit} {value}"

        await ctx.send(
            card_str + description + "\n" + "Score: " + str(self.score), hidden=True
        )
        return str(self.score)

    async def show1_dealer(self, ctx):
        card_str = "**Dealer's hand:**\n"
        card = self.cards[0]

        suit, value = await card.show(ctx)
        card_str += f"\n{suit} {value}"
        await ctx.send(card_str + "\n", hidden=True)

    async def result(self, ctx):
        description = ""
        card_str = ""
        card_str = "**Dealer's hand:**\n" if self.isDealer else "**Your hand:**\n"
        for i in self.cards:
            suit, value = await i.show(ctx)
            description += f"\n{suit} {value}"

        description = "\n" + card_str + description + "\n" + "Score: " + str(self.score)

        return description


class Blackjack:
    def __init__(self, bot):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        self.bot = bot

    async def show_result(self, ctx, description, desc2):
        await ctx.send("**Results:**" + "\n" + description + desc2)

    async def on_win(self, ctx):
        exp = db.find({"_id": ctx.author.id})[0]["EXP"]

        exp_gain = exp + 150

        db.update_one({"_id": ctx.author.id}, {"$set": {"EXP": exp_gain}})
        await ctx.send("✨+150 EXP", hidden=True)

    async def on_lose(self, ctx):
        exp = db.find({"_id": ctx.author.id})[0]["EXP"]

        exp_gain = exp + 50

        db.update_one({"_id": ctx.author.id}, {"$set": {"EXP": exp_gain}})
        await ctx.send("✨+50 EXP", hidden=True)

    async def on_tie(self, ctx):
        exp = db.find({"_id": ctx.author.id})[0]["EXP"]

        exp_gain = exp + 100

        db.update_one({"_id": ctx.author.id}, {"$set": {"EXP": exp_gain}})
        await ctx.send("✨+100 EXP", hidden=True)

    async def play(self, ctx):
        p_status = self.player.deal()
        d_status = self.dealer.deal()

        await self.player.show(ctx)
        await self.dealer.show1_dealer(ctx)

        if p_status == 1:
            description = await self.player.result(ctx)
            desc2 = await self.dealer.result(ctx)

            await self.show_result(ctx, description, desc2)

            await ctx.send("Player has a blackjack!")

            await self.on_win(ctx)

            return 1

        # if d_status == 1:
        #     await self.dealer.show(ctx)
        #     await ctx.send("Dealer has a blackjack!", hidden=True)
        #     return 1

        bust = 0
        await ctx.send("Hit or Stand?", hidden=True)
        cmd = await self.bot.wait_for(
            "message", check=lambda message: message.author == ctx.author
        )

        while cmd.content.lower() != "stand":
            await asyncio.sleep(0.1)
            if cmd.content.lower() == "hit":
                bust = self.player.hit()
                await self.player.show(ctx)

            if bust == 1:
                description = await self.player.result(ctx)
                desc2 = await self.dealer.result(ctx)

                await self.show_result(ctx, description, desc2)

                await ctx.send("Player busted.")

                await self.on_lose(ctx)

                return 1

            elif p_status == 1:
                description = await self.player.result(ctx)
                desc2 = await self.dealer.result(ctx)

                await self.show_result(ctx, description, desc2)

                await ctx.send("Player has a blackjack!")

                await self.on_win(ctx)

            else:
                await ctx.send("Hit or Stand?", hidden=True)
                cmd = await self.bot.wait_for(
                    "message", check=lambda message: message.author == ctx.author
                )

        await self.dealer.show(ctx)

        if d_status == 1:
            description = await self.player.result(ctx)
            desc2 = await self.dealer.result(ctx)

            await self.show_result(ctx, description, desc2)

            await ctx.send("Dealer got blackjack!")

            await self.on_lose(ctx)

            return 1

        while self.dealer.check_score() < 17:
            await asyncio.sleep(0.3)
            await ctx.send("Dealer has hit...", hidden=True)
            if self.dealer.hit() == 1:
                await self.dealer.show(ctx)

                description = await self.player.result(ctx)
                desc2 = await self.dealer.result(ctx)

                await self.show_result(ctx, description, desc2)

                await ctx.send("Dealer busted, Player wins!")

                await self.on_win(ctx)

                return 1

            elif d_status == 1:
                description = await self.player.result(ctx)
                desc2 = await self.dealer.result(ctx)

                await self.show_result(ctx, description, desc2)

                await ctx.send("Dealer got blackjack!")

                await self.on_lose(ctx)

                return 1

            await self.dealer.show(ctx)

        if self.dealer.check_score() == self.player.check_score():
            description = await self.player.result(ctx)
            desc2 = await self.dealer.result(ctx)

            await self.show_result(ctx, description, desc2)

            await ctx.send("Tie!")

            await self.on_tie(ctx)

        elif self.dealer.check_score() > self.player.check_score():
            description = await self.player.result(ctx)
            desc2 = await self.dealer.result(ctx)

            await self.show_result(ctx, description, desc2)

            await ctx.send("Dealer wins.")

            await self.on_lose(ctx)

        elif self.dealer.check_score() < self.player.check_score():
            description = await self.player.result(ctx)
            desc2 = await self.dealer.result(ctx)

            await self.show_result(ctx, description, desc2)

            await ctx.send("Player wins.")

            await self.on_win(ctx)


# b.play()

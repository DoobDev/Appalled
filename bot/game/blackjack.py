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
#from bot.bot import SlashCommand


class Card:
    def __init__(self, value, suit):
        self.cost = value
        self.value = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"][
            value - 1
        ]
        self.suit = "❤️◆☘️♠️"[suit]

    def price(self):
        if self.cost >= 10:
            return 10
        elif self.cost == 1:
            return 11
        return self.cost

    async def show(self, ctx):
        print(self.suit + self.value)
        await ctx.send(f"{self.suit} + {self.value}")


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

    async def show(self, ctx):
        if self.isDealer:
            await ctx.send("Dealer's Cards")
        else:
            await ctx.send("Player's Cards")

        for i in self.cards:
            await i.show(ctx)

        await ctx.send("Score: " + str(self.score))


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)

    async def play(self, ctx):
        p_status = self.player.deal()
        d_status = self.dealer.deal()

        await self.player.show(ctx)

        if p_status == 1:
            await ctx.send("Player has a blackjack!")
            if d_status == 1:
                await ctx.send("Dealer has a blackjack!")
            return 1

        await self.hit_or_stand(ctx)

        await self.dealer.show(ctx)

        if d_status == 1:
            await ctx.send("Dealer got blackjack!")
            return 1

        while self.dealer.check_score() > 17:
            if self.dealer.hit() == 1:
                self.dealer.show(ctx)
                await ctx.send("Dealer busted.")
                return 1
            else:
                await ctx.send("Dealer Hit..")
            await self.dealer.show(ctx)

        if self.dealer.check_score() == self.player.check_score():
            await ctx.send("Tie!")
        elif self.dealer.check_score() > self.player.check_score():
            await ctx.send("Dealer wins.")
        elif self.dealer.check_score() < self.player.check_score():
            await ctx.send("Player wins.")


b = Blackjack()
# b.play()

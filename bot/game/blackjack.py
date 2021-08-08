# TODO: make it work?

from models.deck import Deck
from models.player import Player


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)

    def play(self):
        p_status = self.player.deal()
        d_status = self.dealer.deal()

        self.player.show()

        if p_status == 1:
            print("Player has a blackjack!")
            if d_status == 1:
                print("Dealer has a blackjack!")
            return 1

        cmd = ""
        while cmd != "Stand":
            bust = 0
            cmd = input("Hit or Stand? ")

            if cmd == "Hit":
                bust = self.player.hit()
                self.player.show()
            if bust == 1:
                print("Player busted.")
                return 1

        print("\n")
        self.dealer.show()

        if d_status == 1:
            print("Dealer got blackjack!")
            return 1

        while self.dealer.check_score() > 17:
            if self.dealer.hit() == 1:
                self.dealer.show()
                print("Dealer busted.")
                return 1
            else:
                print("Dealer Hit..")
            self.dealer.show()

        if self.dealer.check_score() == self.player.check_score():
            print("Tie!")
        elif self.dealer.check_score() > self.player.check_score():
            print("Dealer wins.")
        elif self.dealer.check_score() < self.player.check_score():
            print("Player wins.")


b = Blackjack()
b.play()

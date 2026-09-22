import cards as c

debug = False

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = self.load_deck(deck)
    def load_deck(self, deck):
        new_deck = []
        for card in deck:
            new_deck.append(c.get_card(card))
        return new_deck

if debug:
    print("nothing")
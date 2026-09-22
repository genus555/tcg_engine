from enum import Enum
from pathlib import Path
import json

loaded_cards = []
debug = True

class CardType(Enum):
    SPELL = 1
    GATE = 2


class Card:
    def __init__(self, data):
        self.data = data
        self.name = self.data["name"]
        self.type = self.data["type"]
        self.effect = self.card_json_to_code()
    def card_json_to_code(self):
        code = f"""def {self.name}():
            {self.data["func"]}
        """
        effects = {}
        exec(code, effects)
        return effects[f"{self.name}"]
    def debug(self):
        print(f"Name: {self.name}\nEffect: {self.effect}\nType: {self.type.name}\nFull JSON: {self.data}")

def check_if_loaded(c: Card):
    if any(x.name == c.name for x in loaded_cards):
        if debug:
            print(f"Card \"{c.name}\" is loaded")
        return True
    return False

def getCard(name):
    file = name.replace(" ", "_")
    file = Path("cards") / file
    with open(file, "r") as f:
        card = Card(json.load(f))
        if not check_if_loaded(card):
            loaded_cards.append(card)

getCard("Dust Tornado")
getCard("Pot of Greed")
getCard("Dust Tornado")
getCard("Pot of Greed")

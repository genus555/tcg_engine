from enum import Enum
from pathlib import Path
import json

loaded_cards = []
debug = False

class CardType(Enum):
    SPELL = 1
    GATE = 2


class Card:
    def __init__(self, data):
        self.name = data["name"]
        self.type = data["type"]
        self.effect = self.card_json_to_code(data)
    def card_json_to_code(self, data):
        code = f"""def {self.name}():
            {data["func"]}
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

def get_card(name):
    file = name.replace(" ", "_")
    file = Path("cards") / file
    try:
        with open(file, "r") as f:
            card = Card(json.load(f))
            if not check_if_loaded(card):
                loaded_cards.append(card)
    except FileNotFoundError:
        return None
    return card

def check_exists(name):
    check = get_card(name)
    if check == None:
        return False
    return True

if debug:
    get_card("Dust Tornado")
    get_card("Pot of Greed")
    get_card("Dust Tornado")
    get_card("Pot of Greed")

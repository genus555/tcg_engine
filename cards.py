from enum import Enum
from pathlib import Path
import gamelogic as gl
import json
import textwrap

loaded_cards = []
debug = False

class CardType(Enum):
    SPELL = 1
    GATE = 2


class Card:
    def __init__(self, data):
        self.name = data["name"]
        self.func_name = data["func_name"]
        self.type = data["type"]
        self.description = data["description"]
        self.effect = self.card_json_to_code(data)

    def card_json_to_code(self, data):
        func = "\n".join(data["func"])
        func = textwrap.indent(func, "    ")
        code = f"""def {self.func_name}(ps, os, chain, ordered_chain):
{func}
        """
        effects = globals().copy()
        exec(code, effects)
        return effects[f"{self.func_name}"]

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"Name: {self.name}\nEffect: {self.effect}\nType: {self.type.name}\nFull JSON: {self.data}"

def check_if_loaded(c: Card):
    if any(x.name == c.name for x in loaded_cards):
        if debug:
            print(f"Card \"{c.name}\" is loaded")
        return True
    return False

def get_card(name):
    file = name
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

def check_and_remove_from_deck(card_name, ps):
    if check_exists(card_name):
        deck = ps["deck"]
        for c in deck:
            if card_name.strip().lower() == c.name.strip().lower():
                deck.remove(c)
                gl.shuffle_deck(ps["deck"])
                return True
    return False

def resolve(card_name, ps, os, chain):
    ordered_chain = chain[::-1]
    card = get_card(card_name)
    card.effect(ps, os, chain, ordered_chain)

if debug:
    get_card("Trash Card")
    get_card("Pot of Greed")

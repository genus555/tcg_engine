import player as p
import cards as c
import gamestate
import random
import sys

debug = False

def init_debug_players():
    deck1 = []
    deck2 = []
    for i in range(2):
        deck1.append("Trash Card")
        deck2.append("Trash Card")
        deck1.append("Nothing")
        deck2.append("Nothing")
        deck1.append("Pot of Greed")
        deck2.append("Pot of Greed")
        deck1.append("Scry")
        deck2.append("Scry")
        deck1.append("Cheeky Gnab")
        deck2.append("Cheeky Gnab")
        deck1.append("Trickery")
        deck2.append("Trickery")
        deck1.append("Cut")
        deck2.append("Cut")
        deck1.append("Flub You")
        deck2.append("Flub You")
        deck1.append("Double Edged")
        deck2.append("Double Edged")
        deck1.append("Recovery")
        deck2.append("Recovery")
    for i in range(10):
        deck1.append("A Brick")
        deck2.append("A Brick")
    p1 = p.Player('Charlie', deck1)
    p2 = p.Player('Karen(Momonga)', deck2)
    return [p1, p2]

def select_rand_num(range):
    return random.randint(0, range)

def shuffle_deck(deck):
    random.shuffle(deck)

def find_used_cards(ps):
    all_cards = ps["hand"] + ps["deck"]
    used_cards = ps["og_deck"].copy()
    for card in ps["og_deck"]:
        if card in all_cards:
            used_cards.remove(card)
    return used_cards

def add_to_hand(card_obj, ps):
    ps["hand"].append(card_obj)

def discard_from_hand(ps):
    while True:
        print("Choose a card to discard from your hand.")
        print([card.name for card in ps["hand"]])
        card_name = input("> ")
        check = in_hand(card_name, ps)
        if check:
            for c in ps["hand"]:
                if card_name.strip().lower() == c.name.strip().lower():
                    ps["hand"].remove(c)
                    return
        else:
            print(f"{card_name} is not a card in your hand.")

def end_game():
    sys.exit()

def draw(ts):
    deck = ts["deck"]
    hand = ts["hand"]
    if not deck:
        print(f"The deck is empty, {ts["name"]} wins!")
        end_game()
    drawn_card = deck.pop()
    hand.append(drawn_card)
    ts["deck"] = deck
    ts["hand"] = hand
    return ts

def play(card, ts):
    hand = ts["hand"]
    for c in hand:
        if card.strip().lower() == c.name.strip().lower():
            hand.remove(c)
            return

def in_hand(card, ps):
    for c in ps["hand"]:
        if card.strip().lower() == c.name.strip().lower():
            return True
    return False

def chain(gs, ts, played_card):
    chain = []
    played_card = " ".join(played_card)
    if not c.check_exists(played_card):
        print(f"{played_card} is not a valid card")
        return None
    if not in_hand(played_card, ts):
        print(f"{played_card} is not in your hand")
        return None
    if gs.p1 == ts:
        play(played_card, gs.p1)
        chain.append([played_card, gs.p1, gs.p2])
    if gs.p2 == ts:
        play(played_card, gs.p2)
        chain.append([played_card, gs.p2, gs.p1])
    temp_turn = gs.turn_num + 1
    while True:
        #chain state: state of person who started chain
        cs = {}
        #opponent state: state of opponent of person who started chain
        os = {}
        if temp_turn % 2 == 1:
            cs = gs.p1
            os = gs.p2
        else:
            cs = gs.p2
            os = gs.p1
        print(f"Current chain:", [card[0] for card in chain])
        print(f"{cs["name"]}'s Hand:")
        gamestate.show_hand(cs["hand"])
        command = input("> ").lower()
        command = command.split()
        match command[0]:
            case "play" | "pl":
                card = command[1:]
                card = " ".join(card)
                check = c.check_exists(card)
                check2 = in_hand(card, cs)
                if check:
                    if check2:
                        play(card, cs)
                        chain.append([card, cs, os])
                        temp_turn += 1
                    else:
                        print(f"{card} is not in your hand.")
                else:
                    print(f"{card} is not a valid card.")
            case "describe" | "d":
                card = " ".join(command[1:])
                if not c.check_exists(card):
                    print(f"{card} is not a valid card")
                else:
                    card_obj = c.get_card(card)
                    print(f"{card_obj.name}: {card_obj.description}")
            case "pass" | "p":
                return chain

if debug:
    players = init_debug_players()
    p1 = players[0]
    p2 = players[1]
    print(f"{p1.name}'s deck:\n{len(p1.deck)}")
    print(f"{p2.name}'s deck:\n{len(p2.deck)}")
    p1_deck = p1.deck
    p2_deck = p2.deck
    shuffle_deck(p1_deck)
    shuffle_deck(p2_deck)
    print(f"""\nPost Shuffle:
{p1.name}'s deck:\n{len(p1_deck)}
{p2.name}'s deck:\n{p2_deck}""")
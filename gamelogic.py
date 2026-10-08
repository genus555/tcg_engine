import player as p
import cards as c
import gamestate
import random

debug = False

def init_debug_players():
    deck1 = []
    deck2 = []
    for i in range(5):
        deck1.append("Dust Tornado")
        deck2.append("Dust Tornado")
        deck1.append("Nothing")
        deck2.append("Nothing")
        deck1.append("Pot of Greed")
        deck2.append("Pot of Greed")
        deck1.append("Scry")
        deck2.append("Scry")
    p1 = p.Player('Charlie', deck1)
    p2 = p.Player('Karen(Momonga)', deck2)
    return [p1, p2]

def shuffle_deck(deck):
    random.shuffle(deck)

def draw(ts):
    deck = ts["deck"]
    hand = ts["hand"]
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
            return c

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
            case "play":
                card = command[1:]
                card = " ".join(card)
                check = c.check_exists(card)
                check2 = in_hand(card, cs)
                if check:
                    if check2:
                        played = play(card, cs)
                        chain.append([card, cs, os])
                        temp_turn += 1
                    else:
                        print(f"{card} is not in your hand.")
                else:
                    print(f"{card} is not a valid card.")
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
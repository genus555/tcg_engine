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
        if card.lower() == c.name.lower():
            hand.remove(c)
            break
    ts["hand"] = hand

def chain(gs, ts, played_card):
    played_card = " ".join(played_card)
    print(played_card)
    if not c.check_exists(played_card):
        print(f"{played_card} is not a valid card")
    play(played_card, ts)
    chain = []
    chain.append(played_card)
    temp_turn = gs.turn_num + 1
    while True:
        cs = {}
        if temp_turn % 2 == 1:
            cs = gs.p1
        else:
            cs = gs.p2
        print(f"Current chain: {chain}")
        print(f"{cs["name"]}'s Hand:")
        gamestate.show_hand(cs["hand"])
        command = input("> ").lower()
        command = command.split()
        match command[0]:
            case "play":
                card = command[1:]
                card = " ".join(card)
                check = c.check_exists(card)
                if check:
                    play(card, cs)
                    temp_turn += 1
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
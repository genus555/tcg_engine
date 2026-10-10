import cards as c
import gamelogic as gl
import gamestate

import time

debug = True

def main():
    if debug:
        players = gl.init_debug_players()
        p1_name = players[0].name
        p2_name = players[1].name
        p1_d = players[0].deck
        p2_d = players[1].deck
        gl.shuffle_deck(p1_d)
        gl.shuffle_deck(p2_d)
        p1 = {}
        p1["name"] = p1_name
        p1["og_deck"] = p1_d.copy()
        p1["deck"] = p1_d.copy()
        p1["hand"] = []
        p2 = {}
        p2["name"] = p2_name
        p2["og_deck"] = p2_d.copy()
        p2["deck"] = p2_d.copy()
        p2["hand"] = []
        gs = gamestate.GameState(p1, p2)
    print("Type help for a list of available commands")
    while True:
        turn = gs.get_turn_state()
        if gs.turn_num > 1:
            if not gs.drew_for_turn:
                gl.draw(turn)
                gs.drew_for_turn = True
        if not turn["deck"]:
                    print(f"The deck is empty, {turn["name"]} wins!")
                    sys.exit()
        if debug:
            show_turn(turn)
        print(f"{turn["name"]}'s turn.")
        print(f"{turn["name"]}'s Hand:")
        gamestate.show_hand(turn["hand"])
        command = input("> ").lower()
        if not command.strip():
            continue
        command = command.split()
        match command[0]:
            case "play" | "pl":
                if gs.card_used:
                    print("Card already used this turn.")
                else:
                    chain = gl.chain(gs, turn, command[1:])
                    if chain:
                        resolve_chain(chain)
                        gs.card_used = True
            case "describe" | "d":
                card = " ".join(command[1:])
                if not c.check_exists(card):
                    print(f"{card} is not a valid card")
                else:
                    card_obj = c.get_card(card)
                    print(f"{card_obj.name}: {card_obj.description}")
            case "used" | "u":
                gl.print_used_cards(gs.get_turn_state())
            case "pass" | "p":
                gs.turn_num += 1
                gs.card_used = False
                gs.drew_for_turn = False
            case "help" | "h":
                gl.help()
            case "quit" | "q":
                gl.end_game()
            case _:
                print(f'{command[0]} is not a recognized command. Type \'help\' for a list of commands.')

def show_turn(turn):
    print(turn["name"])
    print(len(turn["deck"]))
    print(len(turn["hand"]))

def resolve_chain(chain):
    while chain:
        played = chain.pop()
        c.resolve(played[0], played[1], played[2], chain)
        print(f"Current chain: {[card[0] for card in chain]}")
        time.sleep(3)


if __name__ == '__main__':
    main()
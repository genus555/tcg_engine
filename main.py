import gamelogic as gl
import gamestate
import sys

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
        p1["deck"] = p1_d
        p1["hand"] = []
        p2 = {}
        p2["name"] = p2_name
        p2["deck"] = p2_d
        p2["hand"] = []
        gs = gamestate.GameState(p1, p2)
    while True:
        turn = gs.get_turn_state()
        if gs.turn_num > 1:
            if gs.drew_for_turn:
                gl.draw(turn)
                gs.drew_for_turn = True
        if debug:
            show_turn(turn)
        print(f"{turn["name"]}'s turn.")
        print(f"{turn["name"]}'s Hand:")
        gamestate.show_hand(turn["hand"])
        command = input("> ").lower()
        command = command.split()
        match command[0]:
            case "play":
                if gs.card_used:
                    print("Card already used this turn.")
                else:
                    chain = gl.chain(gs, turn, command[1:])
                    print(chain)
                    gs.card_used = True
            case "pass" | "p":
                gs.turn_num += 1
                gs.card_used = False
                gs.drew_for_turn = False
            case "quit" | "q":
                sys.exit()

def show_turn(turn):
    print(turn["name"])
    print(len(turn["deck"]))
    print(len(turn["hand"]))


if __name__ == '__main__':
    main()
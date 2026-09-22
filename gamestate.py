import gamelogic as gl
import player as p

class GameState:
    def __init__(self, p1_state, p2_state):
        self.p1 = p1_state
        self.p2 = p2_state
        self.turn_num = 1
        self.game_start()

    def game_start(self):
        for i in range(5):
            self.p1 = gl.draw(self.p1)
            self.p2 = gl.draw(self.p2)

    def get_turn_state(self):
        if self.turn_num % 2 == 1:
            return self.p1
        else:
            return self.p2

def show_hand(hand):
    hand_names = []
    for card in hand:
        card = card.name.replace("_", " ")
        hand_names.append(card)
    print(hand_names)
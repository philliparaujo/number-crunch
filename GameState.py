from features import *


class GameState:
    def __init__(self):
        self.score = 0
        self.turn = 0
        self.actions = ACTIONS_START
        self.target = TARGET_START
        self.hp = HP_START
        self.free_reroll = True

        self.scores = []
        self.max_score = 0
        self.next_target = NEXT_TARGET_START

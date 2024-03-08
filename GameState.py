from features import *
from utils import *


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

    # Gets
    def get_score(self):
        return self.score

    def get_turn(self):
        return self.turn

    def get_actions(self):
        return self.actions

    def get_target(self):
        return self.target

    def get_hp(self):
        return self.hp

    def get_free_reroll(self):
        return self.free_reroll

    def get_max_score(self):
        return self.max_score

    def get_next_target(self):
        return self.next_target

    # Updates
    def update_score(self, cells):
        self.score = calculate_score(cells)
        self.max_score = max(self.max_score, self.score)

    def decrease_actions(self, amount):
        self.actions -= amount

    # Simple checks
    def game_over(self):
        return self.hp <= 0

    def will_take_damage(self):
        return self.target > self.score

    def can_reroll(self):
        return self.free_reroll or self.actions > 0

    # Game procedures
    def end_turn(self):
        self.scores += [str(self.score)]
        self.hp -= max(0, self.target - self.score)
        self.turn += 1
        self.actions = ACTIONS_START
        self.target = fetch_target_score(threshold, self.turn, self.target)
        self.next_target = fetch_target_score(
            threshold, self.turn + 1, self.next_target
        )
        self.free_reroll = True

    def reroll(self):
        if self.free_reroll:
            self.free_reroll = False
        else:
            self.actions -= 1

    # Misc
    def print_scores(self):
        print(self.scores)

    def reset_texts(self, texts):
        for text in texts:
            text.reset(self.turn)

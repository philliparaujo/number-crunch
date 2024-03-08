from features import *
from utils import *


class GameState:
    def __init__(self):
        self.restart()

    # Gets
    def score(self):
        return self._score

    def turn(self):
        return self._turn

    def actions(self):
        return self._actions

    def target(self):
        return self._target

    def hp(self):
        return self._hp

    def free_reroll(self):
        return self._free_reroll

    def max_score(self):
        return self._max_score

    def next_target(self):
        return self._next_target

    def started(self):
        return self._started

    def game_over(self):
        return self._game_over

    def exited(self):
        return self._exited

    # Updates
    def update_score(self, cells):
        self._score = calculate_score(cells)
        self._max_score = max(self._max_score, self._score)

    def decrease_actions(self, amount):
        self._actions -= amount

    def set_started(self, started):
        self._started = started

    def set_game_over(self, game_over):
        self._game_over = game_over

    def set_exited(self, exited):
        self._exited = exited

    # Simple checks
    def is_game_over(self):
        return self._hp <= 0

    def will_take_damage(self):
        return self._target > self._score

    def can_reroll(self):
        return self._free_reroll or self._actions > 0

    def can_drop(self, dragging):
        return dragging and self._actions >= dragging.cost

    # Game procedures
    def restart(self):
        self._score = 0
        self._turn = 0
        self._actions = ACTIONS_START
        self._target = TARGET_START
        self._hp = HP_START
        self._free_reroll = True

        self._scores = []
        self._max_score = 0
        self._next_target = NEXT_TARGET_START

        self._started = False
        self._game_over = True
        self._exited = False

    def end_turn(self):
        self._scores += [str(self._score)]
        self._hp -= max(0, self._target - self._score)
        self._turn += 1
        self._actions = ACTIONS_START
        self._target = fetch_target_score(threshold, self._turn, self._target)
        self._next_target = fetch_target_score(
            threshold, self._turn + 1, self._next_target
        )
        self._free_reroll = True

    def reroll(self):
        if self._free_reroll:
            self._free_reroll = False
        else:
            self._actions -= 1

    # Misc
    def print_scores(self):
        print(self._scores)

    def reset_texts(self, texts):
        for text in texts:
            text.reset(self._turn)


game = GameState()

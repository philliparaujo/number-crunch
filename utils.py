import random

from ui import *


def random_choice(weights, index):
    if index > len(weights) - 1:
        index = len(weights) - 1
    return random.choices(weights[index][0], weights[index][1])[0]


def min_choice(weights, index):
    if index > len(weights) - 1:
        index = len(weights) - 1
    return min(weights[index][0])


def max_choice(weights, index):
    if index > len(weights) - 1:
        index = len(weights) - 1
    return max(weights[index][0])


# Sums all values in cell array (including bonuses), returns the sum
def calculate_score(cells):
    score = 0
    for i in range(len(cells)):
        cell = cells[i]
        score += cell.value
        for j in range(i + 1, len(cells)):
            if cell.value == cells[j].value:
                score += cell.value

    return score


# Displays the range of possible number values for the shop
def get_shop_range(weights, turn):
    return (
        "("
        + str(min_choice(weights, turn))
        + "-"
        + str(max_choice(weights, turn))
        + ")"
    )


# Return difference in scores between two boards
def calculate_score_diff(cells, cells_copy):
    return calculate_score(cells_copy) - calculate_score(cells)


def cost(value):
    return "(" + str(value) + ")"


def preview_text(value):
    return "(" + ("+" if value >= 0 else "-") + str(abs(value)) + ")"


def center_x(button):
    return button.x + BUTTON_WIDTH / 2


def above_y(button):
    return button.y - 15

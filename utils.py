import random


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


# Adds up all values in cell array (including bonuses), returns the sum
def calculate_score(cells):
    score = 0
    for i in range(len(cells)):
        cell = cells[i]
        score += cell.value
        for j in range(i + 1, len(cells)):
            if cell.value == cells[j].value:
                score += cell.value

    return score


# Performs an add on the two selected cells
# Assumes that add_check is successful
def add_cells(cells):
    selected_cells = list(filter(lambda cell: cell.selected, cells))
    if len(selected_cells) == 2:
        first_cell = selected_cells[0]
        second_cell = selected_cells[1]
        first_cell.value += second_cell.value
        second_cell.value = 0

        first_cell.selected = False
        second_cell.selected = False

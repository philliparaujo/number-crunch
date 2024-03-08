import random
import pygame
import copy
from pygame.locals import *
from colors import *
from components import *
from features import *
from ui import *
from sounds import *
from GameState import *

from utils import *

# Mouse variables
clicking = False
dragging = None


def main():
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    # Game variables
    game_state = GameState()

    # Mouse variables
    global clicking, dragging

    # Initialize sound effects

    # Button functions
    def end_turn():
        nonlocal game_state
        if game_state.target > game_state.score:
            damage_sfx.play()

        game_state.end_turn()
        game_state.reset_texts(texts)

        print(game_state.scores)

    def reroll_check():
        nonlocal game_state
        return game_state.free_reroll or game_state.actions > 0

    def reroll():
        nonlocal game_state
        if reroll_check():
            game_state.reroll()
            game_state.reset_texts(texts)

    def add_check():
        nonlocal cells
        num_selected = 0
        for cell in cells:
            if cell.selected:
                num_selected += 1

        return num_selected == 2

    def add():
        nonlocal cells
        if add_check():
            add_sfx.play()
            add_cells(cells)

    # UI components
    add_button = Button(
        screen,
        "ADD",
        PURPLE,
        LIGHT_PURPLE,
        SHOP_X,
        400,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        add,
        add_check,
    )
    reroll_button = Button(
        screen,
        "REROLL",
        BLUE,
        LIGHT_BLUE,
        SHOP_X + 120,
        400,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        reroll,
        reroll_check,
    )
    end_turn_button = Button(
        screen,
        "END TURN",
        DARK_GREEN,
        GREEN,
        SHOP_X + 240,
        400,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        end_turn,
    )
    buttons = [add_button, reroll_button, end_turn_button]

    level_one_text = DraggableText(
        screen,
        str(random_choice(level_one_weights, 0)),
        NUMBER_SIZE,
        SHOP_X + SHOP_WIDTH / 2,
        85,
        1,
        level_one_weights,
    )
    level_two_text = DraggableText(
        screen,
        str(random_choice(level_two_weights, 0)),
        NUMBER_SIZE,
        SHOP_X + SHOP_WIDTH / 2,
        165,
        2,
        level_two_weights,
    )
    level_three_text = DraggableText(
        screen,
        str(random_choice(level_three_weights, 0)),
        NUMBER_SIZE,
        SHOP_X + SHOP_WIDTH / 2,
        245,
        3,
        level_three_weights,
    )
    texts = [level_one_text, level_two_text, level_three_text]

    cells = create_grid(
        screen, GRID_X, 60, SQUARE_SIZE, GRID_WIDTH, GRID_HEIGHT, GRID_GAP
    )

    # Main loop
    game_over = False
    exited = False
    while not game_over and not exited:
        if game_state.game_over():
            game_over = True

        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()

        # Draw title, game state, board, shop, and buttons
        draw_centered_text(screen, TITLE, TITLE_SIZE, SCREEN_WIDTH / 2, 20)
        draw_game_state(screen, game_state)

        if not handle_add_preview(
            screen, cells, game_state
        ):  # Prevents preview overlap
            handle_buy_preview(screen, cells, mouse_pos, game_state)
        handle_end_turn_preview(screen, mouse_pos, end_turn_button, game_state)

        for cell in cells:
            cell.draw(mouse_pos, dragging, game_state.actions)

        draw_shop(screen, texts, game_state)
        draw_buttons(screen, buttons, mouse_pos, game_state)

        # Handle text dragging of shop items
        for text in texts:
            if pygame.mouse.get_pressed()[0]:
                dragging = text.drag(mouse_pos, dragging)

        for event in pygame.event.get():
            # Handle closing out of game
            if event.type == pygame.QUIT:
                exited = True

            # Handle click events and allow for dragging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event, buttons, cells, mouse_pos)

            # Handle drop events
            elif event.type == pygame.MOUSEBUTTONUP:
                actions = handle_mouse_release(event, cells, mouse_pos, game_state)

        game_state.update_score(cells)

        pygame.display.flip()

    # Game over screen
    while game_over and not exited:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exited = True

        draw_game_over_screen(screen, game_state)


def draw_game_state(screen, game_state):
    score_text = "Score: " + str(game_state.score)
    turn_text = "Turn: " + str(game_state.turn)
    actions_text = "Actions: " + str(game_state.actions)
    target_text = "Target: " + str(game_state.target)
    hp_text = "HP: " + str(game_state.hp)

    draw_text(screen, score_text, STATE_SIZE, STATE_X_1, 380)
    draw_text(screen, turn_text, STATE_SIZE, STATE_X_1, 410)
    draw_text(screen, actions_text, STATE_SIZE, STATE_X_1, 440)
    draw_text(screen, target_text, STATE_SIZE, STATE_X_2, 380)
    draw_text(screen, hp_text, STATE_SIZE, STATE_X_2, 410)


def get_shop_range(weights, turn):
    return (
        "("
        + str(min_choice(weights, turn))
        + "-"
        + str(max_choice(weights, turn))
        + ")"
    )


def draw_shop(screen, texts, game_state):
    draw_rect(screen, GRAY, SHOP_X, 60, SHOP_WIDTH, SHOP_HEIGHT)
    draw_text(screen, "(1)", COST_SIZE, SHOP_X + 30, 75, DARK_GREEN)
    draw_text(
        screen,
        get_shop_range(level_one_weights, game_state.turn),
        COST_SIZE,
        SHOP_X + 250,
        75,
        DARK_GRAY,
    )

    draw_rect(screen, GRAY, SHOP_X, 140, SHOP_WIDTH, SHOP_HEIGHT)
    draw_text(screen, "(2)", COST_SIZE, SHOP_X + 30, 155, DARK_GREEN)
    draw_text(
        screen,
        get_shop_range(level_two_weights, game_state.turn),
        COST_SIZE,
        SHOP_X + 250,
        155,
        DARK_GRAY,
    )

    draw_rect(screen, GRAY, SHOP_X, 220, SHOP_WIDTH, SHOP_HEIGHT)
    draw_text(screen, "(3)", COST_SIZE, SHOP_X + 30, 235, DARK_GREEN)
    draw_text(
        screen,
        get_shop_range(level_three_weights, game_state.turn),
        COST_SIZE,
        SHOP_X + 250,
        235,
        DARK_GRAY,
    )

    for text in texts:
        text.draw()


def draw_buttons(screen, buttons, mouse_pos, game_state):
    add_button = buttons[0]
    reroll_button = buttons[1]

    for button in buttons:
        button.draw(mouse_pos)

    # Add button and reroll button costs
    draw_centered_text(
        screen,
        "(0)",
        COST_SIZE,
        add_button.x + BUTTON_WIDTH / 2,
        add_button.y - 15,
        DARK_GREEN,
    )
    draw_centered_text(
        screen,
        "(0)" if game_state.free_reroll else "(1)",
        COST_SIZE,
        reroll_button.x + BUTTON_WIDTH / 2,
        reroll_button.y - 15,
        DARK_GREEN,
    )


def handle_buy_preview(screen, cells, mouse_pos, game_state):
    score_text = "Score: " + str(game_state.score)
    cells_copy = [cell.copy() for cell in cells]
    for cell in cells_copy:
        if (
            cell.willDropSucceed(mouse_pos)
            and dragging
            and game_state.actions >= dragging.cost
        ):
            cell.drop(mouse_pos, dragging, False)
            score_diff = calculate_score(cells_copy) - calculate_score(cells)
            score_preview = (
                "(" + ("+" if score_diff >= 0 else "-") + str(abs(score_diff)) + ")"
            )
            score_width = get_text_dimensions(score_text, STATE_SIZE)[0]
            draw_text(
                screen, score_preview, STATE_SIZE, STATE_X_1 + score_width + 5, 380
            )


def handle_add_preview(screen, cells, game_state):
    score_text = "Score: " + str(game_state.score)
    cells_copy = [cell.copy() for cell in cells]
    can_add = sum(1 for cell in cells_copy if cell.selected) == 2
    if can_add:
        add_cells(cells_copy)

        score_diff = calculate_score(cells_copy) - calculate_score(cells)
        score_preview = (
            "(" + ("+" if score_diff >= 0 else "-") + str(abs(score_diff)) + ")"
        )
        score_width = get_text_dimensions(score_text, STATE_SIZE)[0]
        draw_text(screen, score_preview, STATE_SIZE, STATE_X_1 + score_width + 5, 380)
    return can_add


def handle_end_turn_preview(screen, mouse_pos, end_turn_button, game_state):
    target_text = "Target: " + str(game_state.target)
    if end_turn_button.isOver(mouse_pos):
        target_width = get_text_dimensions(target_text, STATE_SIZE)[0]
        draw_text(
            screen,
            "(+" + str(game_state.next_target - game_state.target) + ")",
            STATE_SIZE,
            STATE_X_2 + target_width + 5,
            380,
        )


def handle_mouse_click(event, buttons, cells, pos):
    global clicking
    if event.button == 1 and not clicking:
        for button in buttons:
            button.click(pos)
        for cell in cells:
            cell.click(pos)
        clicking = True


def handle_mouse_release(event, cells, pos, game_state):
    global clicking, dragging
    if event.button == 1:
        clicking = False
        if dragging and game_state.actions >= dragging.cost:
            for cell in cells:
                if cell.willDropSucceed(pos):
                    purchase_sfx.play()
                    cell.drop(pos, dragging)
                    game_state.actions -= dragging.cost
                    dragging = None
        dragging = None
    return game_state.actions


def draw_game_over_screen(screen, game_state):
    screen.fill(BG_COLOR)
    draw_centered_text(screen, "GAME OVER", 72, SCREEN_WIDTH / 2, 80)
    draw_centered_text(
        screen, "Turn: " + str(game_state.turn), 48, SCREEN_WIDTH / 2, 200
    )
    draw_centered_text(
        screen, "Score: " + str(game_state.score), 48, SCREEN_WIDTH / 2, 240
    )
    draw_centered_text(
        screen, "Max Score: " + str(game_state.max_score), 48, SCREEN_WIDTH / 2, 280
    )
    draw_centered_text(
        screen, "Target: " + str(game_state.target), 48, SCREEN_WIDTH / 2, 320
    )
    pygame.display.flip()


if __name__ == "__main__":
    main()

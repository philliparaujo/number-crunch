import pygame
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

    # Mouse variables
    global clicking, dragging

    # Main loop
    while not game.exited():
        # Start screen
        while not game.started() and game.game_over() and not game.exited():
            mouse_pos = pygame.mouse.get_pos()
            game.set_exited(handle_mouse_events([start_button], cells, mouse_pos, game))
            draw_start_screen(screen, mouse_pos, start_button)

        # Gameplay screen
        while not game.game_over() and not game.exited():
            screen.fill(BG_COLOR)

            # Handle events, update game statuses
            mouse_pos = pygame.mouse.get_pos()
            game_buttons = [add_button, reroll_button, end_turn_button]
            game.set_exited(handle_mouse_events(game_buttons, cells, mouse_pos, game))
            game.set_game_over(game.is_game_over())
            game.update_score(cells)

            # Draw title, game state, board, shop, and gane buttons
            draw_centered_text(screen, TITLE, SMALL_TITLE_SIZE, SCREEN_WIDTH / 2, 20)
            draw_game_state(screen, game)

            for cell in cells:
                cell.draw(screen, mouse_pos, dragging, game.actions())

            draw_shop(screen, texts, game)
            draw_game_buttons(screen, game_buttons, mouse_pos, game)

            # Handling UI hover effects
            if not handle_add_preview(screen, cells, game):
                handle_buy_preview(screen, cells, mouse_pos, game)
            handle_end_turn_preview(screen, mouse_pos, end_turn_button, game)

            # Handle text dragging of shop items
            for text in texts:
                if pygame.mouse.get_pressed()[0]:
                    dragging = text.drag(mouse_pos, dragging)

            pygame.display.flip()

        # Game over screen
        while game.game_over() and not game.exited():
            mouse_pos = pygame.mouse.get_pos()
            game.set_exited(
                handle_mouse_events([restart_button], cells, mouse_pos, game)
            )
            draw_game_over_screen(screen, mouse_pos, game, restart_button)


# Draw all game state details (score, turn, actions, target, hp)
def draw_game_state(screen, game):
    score_text = "Score: " + str(game.score())
    turn_text = "Turn: " + str(game.turn())
    actions_text = "Actions: " + str(game.actions())
    target_text = "Target: " + str(game.target())
    hp_text = "HP: " + str(game.hp())

    draw_text(screen, score_text, STATE_SIZE, STATE_X_1, 380)
    draw_text(screen, turn_text, STATE_SIZE, STATE_X_1, 410)
    draw_text(screen, actions_text, STATE_SIZE, STATE_X_1, 440)
    draw_text(screen, target_text, STATE_SIZE, STATE_X_2, 380)
    draw_text(screen, hp_text, STATE_SIZE, STATE_X_2, 410)


# Draw the shop costs, numbers, and rectangles
def draw_shop(screen, texts, game):
    draw_rect(screen, GRAY, SHOP_X, 60, SHOP_WIDTH, SHOP_HEIGHT)
    draw_text(screen, "(1)", COST_SIZE, SHOP_X + 30, 75, DARK_GREEN)
    draw_text(
        screen,
        get_shop_range(level_one_weights, game.turn()),
        COST_SIZE,
        SHOP_X + 250,
        75,
        DARK_GRAY,
    )

    draw_rect(screen, GRAY, SHOP_X, 140, SHOP_WIDTH, SHOP_HEIGHT)
    draw_text(screen, "(2)", COST_SIZE, SHOP_X + 30, 155, DARK_GREEN)
    draw_text(
        screen,
        get_shop_range(level_two_weights, game.turn()),
        COST_SIZE,
        SHOP_X + 250,
        155,
        DARK_GRAY,
    )

    draw_rect(screen, GRAY, SHOP_X, 220, SHOP_WIDTH, SHOP_HEIGHT)
    draw_text(screen, "(3)", COST_SIZE, SHOP_X + 30, 235, DARK_GREEN)
    draw_text(
        screen,
        get_shop_range(level_three_weights, game.turn()),
        COST_SIZE,
        SHOP_X + 250,
        235,
        DARK_GRAY,
    )

    for text in texts:
        text.draw(screen)


# Draw the 'add', 'reroll', and 'end turn' buttons and their costs
def draw_game_buttons(screen, buttons, mouse_pos, game):
    add_button = buttons[0]
    reroll_button = buttons[1]

    for button in buttons:
        button.draw(screen, mouse_pos)

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
        "(0)" if game.free_reroll() else "(1)",
        COST_SIZE,
        reroll_button.x + BUTTON_WIDTH / 2,
        reroll_button.y - 15,
        DARK_GREEN,
    )


# Draw the start screen
def draw_start_screen(screen, pos, start_game_button):
    screen.fill(BG_COLOR)

    draw_centered_text(screen, "Number Crunch", TITLE_SIZE, SCREEN_WIDTH / 2, 180)
    start_game_button.draw(screen, pos)

    pygame.display.flip()


# Draw the game over screen with score details
def draw_game_over_screen(screen, pos, game, restart_button):
    screen.fill(BG_COLOR)
    draw_centered_text(screen, "GAME OVER", TITLE_SIZE, SCREEN_WIDTH / 2, 80)
    draw_centered_text(screen, "Turn: " + str(game.turn()), 48, SCREEN_WIDTH / 2, 160)
    draw_centered_text(screen, "Score: " + str(game.score()), 48, SCREEN_WIDTH / 2, 200)
    draw_centered_text(
        screen,
        "Max Score: " + str(game.max_score()),
        48,
        SCREEN_WIDTH / 2,
        240,
    )
    draw_centered_text(
        screen, "Target: " + str(game.target()), 48, SCREEN_WIDTH / 2, 280
    )
    restart_button.draw(screen, pos)
    pygame.display.flip()


# Given a change in score, draw that change next to score text
def draw_score_diff(screen, score_diff, game):
    score_text = "Score: " + str(game.score())
    score_width = get_text_width(score_text, STATE_SIZE)
    score_preview = "(" + ("+" if score_diff >= 0 else "-") + str(abs(score_diff)) + ")"
    draw_text(screen, score_preview, STATE_SIZE, STATE_X_1 + score_width + 5, 380)


# Given a change in target score, draw that change next to target text
def draw_target_diff(screen, target, target_diff):
    target_text = "Target: " + str(target)
    target_width = get_text_width(target_text, STATE_SIZE)
    draw_text(
        screen,
        "(+" + str(target_diff) + ")",
        STATE_SIZE,
        STATE_X_2 + target_width + 5,
        380,
    )


# Draw what the change in score will be when number is dropped in cell
def handle_buy_preview(screen, cells, mouse_pos, game):
    cells_copy = [cell.copy() for cell in cells]
    for cell in cells_copy:
        if (
            cell.willDropSucceed(mouse_pos)
            and dragging
            and game.actions() >= dragging.cost
        ):
            cell.drop(mouse_pos, dragging, False)
            score_diff = calculate_score_diff(cells, cells_copy)
            draw_score_diff(screen, score_diff, game)


# Draw what change in score will be when add is clicked, return if any change
def handle_add_preview(screen, cells, game):
    cells_copy = [cell.copy() for cell in cells]
    can_add = sum(1 for cell in cells_copy if cell.selected) == 2
    if can_add:
        add_cells(cells_copy)
        score_diff = calculate_score_diff(cells, cells_copy)
        draw_score_diff(screen, score_diff, game)
    return can_add


# Draw what the change in target score will be when end turn is clicked
def handle_end_turn_preview(screen, mouse_pos, end_turn_button, game):
    target = game.target()
    if end_turn_button.isOver(mouse_pos):
        target_diff = game.next_target() - target
        draw_target_diff(screen, target, target_diff)


# Configure buttons and cells to respond to clicks
def handle_mouse_click(event, buttons, cells, pos):
    global clicking
    if event.button == 1 and not clicking:
        for button in buttons:
            button.click(pos)
        for cell in cells:
            cell.click(pos)
        clicking = True


# When mouse released, reset clicking/dragging and drop number in cell if allowed
def handle_mouse_release(event, cells, pos, game):
    global clicking, dragging
    if event.button == 1:
        clicking = False
        if game.can_drop(dragging):
            for cell in cells:
                if cell.willDropSucceed(pos):
                    if dragging.cost == 1:
                        level_one_sfx.play()
                    if dragging.cost == 2:
                        level_two_sfx.play()
                    if dragging.cost == 3:
                        level_three_sfx.play()

                    cell.drop(pos, dragging)
                    game.decrease_actions(dragging.cost)
        dragging = None


# Handles button clicks, cell clicks, and cell drags. Returns true if x-ed out
def handle_mouse_events(buttons, cells, pos, game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event, buttons, cells, pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_release(event, cells, pos, game)


if __name__ == "__main__":
    main()

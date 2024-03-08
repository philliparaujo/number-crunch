from colors import *
from drawer import *
from utils import *
from sounds import *


class Button:
    def __init__(
        self,
        surface,
        text,
        color,
        hover_color,
        x,
        y,
        width,
        height,
        on_click=None,
        check_active=None,
    ):
        self.surface = surface
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click
        self.check_active = check_active

        self.active = True

    def get_updated_colors(self, pos):
        if self.check_active:
            self.active = self.check_active()
        border_color = GRAY if not self.active else BLACK
        color = (
            GRAY
            if not self.active
            else self.hover_color if self.isOver(pos) else self.color
        )
        return border_color, color

    def draw(self, pos):
        border_color, color = self.get_updated_colors(pos)

        draw_rect(self.surface, border_color, self.x, self.y, self.width, self.height)
        draw_rect(
            self.surface,
            color,
            self.x + 2,
            self.y + 2,
            self.width - 4,
            self.height - 4,
        )
        draw_centered_text(
            self.surface,
            self.text,
            int(self.width / 4),
            self.x + self.width / 2,
            self.y + self.height / 2,
            WHITE,
        )

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def click(self, pos):
        if self.isOver(pos):
            if self.on_click:
                self.on_click()
                click_sfx.play()
            return True
        return False


class Cell:
    def __init__(self, surface, x, y, size, color, value=None, selected=False):
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.color = color

        self.value = value
        self.selected = selected

    def draw(self, pos, dragging, actions):
        color = (
            GREEN
            if self.isOver(pos) and dragging and actions >= dragging.cost
            else self.color if not self.selected else RED
        )
        draw_rect(
            self.surface,
            color,
            self.x,
            self.y,
            self.size,
            self.size,
        )
        draw_rect(
            self.surface,
            WHITE,
            self.x + 2,
            self.y + 2,
            self.size - 4,
            self.size - 4,
        )
        if self.value:
            draw_centered_text(
                self.surface,
                str(self.value),
                int(self.size / 3),
                self.x + self.size / 2,
                self.y + self.size / 2,
                (0, 100, 0),
            )

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.size:
            if pos[1] > self.y and pos[1] < self.y + self.size:
                return True
        return False

    def click(self, pos):
        if self.isOver(pos) and self.value:
            self.selected = not self.selected

    # Returns whether drop was successful
    def willDropSucceed(self, pos):
        return self.isOver(pos) and not self.value

    def drop(self, pos, dragging, deleteDragging=True):
        if self.willDropSucceed(pos):
            self.value = int(dragging.text)
            dragging.deleted = deleteDragging

    def copy(self):
        return Cell(
            self.surface,
            self.x,
            self.y,
            self.size,
            self.color,
            self.value,
            self.selected,
        )


class DraggableText:
    def __init__(self, surface, text, size, x, y, cost, weights):
        self.surface = surface
        self.text = text
        self.size = size
        self.x = x
        self.y = y
        self.cost = cost
        self.weights = weights

        self.startX = x
        self.startY = y
        self.deleted = False

    def reset(self, turn):
        self.x = self.startX
        self.y = self.startY
        self.deleted = False

        self.text = str(random_choice(self.weights, turn))

    def draw(self):
        if not self.deleted:
            draw_centered_text(
                self.surface,
                self.text,
                self.size,
                self.x,
                self.y,
                BLACK,
            )

    def drag(self, pos, dragging):
        if self.deleted:
            return dragging

        if abs(pos[0] - self.x) < 30 and abs(pos[1] - self.y) < 30:
            if not dragging or dragging == self:
                dragging = self
                self.x = pos[0]
                self.y = pos[1]
        elif dragging == self:
            self.x = pos[0]
            self.y = pos[1]

        return dragging


def create_grid(surface, left, top, square_size, num_horiz, num_vert, gap, value=0):
    cells = []
    for i in range(num_horiz):
        for j in range(num_vert):
            cell = Cell(
                surface,
                left + i * (square_size + gap),
                top + j * (square_size + gap),
                square_size,
                BLACK,
                value,
            )
            cells.append(cell)
    return cells

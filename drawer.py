import pygame


def draw_text(surface, text, size, x, y, color="black"):
    font = pygame.font.Font(None, size)
    img = font.render(text, True, color)
    surface.blit(img, (x, y))


def draw_centered_text(surface, text, size, x, y, color="black"):
    font = pygame.font.Font(None, size)
    img = font.render(text, True, color)
    img_rect = img.get_rect(center=(x, y))
    surface.blit(img, img_rect)


def get_text_dimensions(text, size):
    font = pygame.font.Font(None, size)
    return font.size(text)


def get_text_width(text, size):
    return get_text_dimensions(text, size)[0]


def draw_list(surface, array, size, x, y, color="black"):
    for i in range(len(array)):
        text = array[i]
        draw_text(surface, text, size, x, y + size * i, color)


def draw_rect(surface, color, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, rect)

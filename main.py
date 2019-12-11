import os
import sys
import pygame
import sqlite3

pygame.init()
# pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 1366
HEIGHT = 768
# STEP = 10
CURSOR = pygame.image.load("images/cursor.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Красная ветка")
pygame.mouse.set_visible(0)
clock = pygame.time.Clock()


def load_image(name, colorKey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorKey is not None:
        if colorKey is -1:
            colorKey = image.get_at((0, 0))
        image.set_colorkey(colorKey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def draw_cursor(x, y):
    screen.blit(CURSOR, (x, y))


def start_screen():
    introText = ["Красная ветка", "",
                 "Старт",
                 "Настройки",
                 "Выход"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    fontBig = pygame.font.Font("Roboto-Black.ttf", 96)
    fontMiddle = pygame.font.Font("Roboto-Black.ttf", 48)
    startButton = Button()
    settingsButton = Button()
    exitButton = Button()
    runningStartScreen = True

    while runningStartScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningStartScreen = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.pressed(pygame.mouse.get_pos()):
                    return
                elif settingsButton.pressed(pygame.mouse.get_pos()):
                    pass
                elif exitButton.pressed(pygame.mouse.get_pos()):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        for i in range(1, 10):
            s = pygame.Surface((length + (i * 2), height + (i * 2)))
            s.fill(color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x - i, y - i, length + i, height + i), width)
            surface.blit(s, (x - i, y - i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, (190, 190, 190), (x, y, length, height), 1)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print("Some button was pressed!")
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


# start_screen()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass

    screen.fill(pygame.Color("black"))
    if pygame.mouse.get_focused():
        draw_cursor(*pygame.mouse.get_pos())
    pygame.display.flip()

    clock.tick(FPS)

terminate()

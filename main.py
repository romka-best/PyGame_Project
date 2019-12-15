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
TIMEBETWEENSTATIONS = 150000
CURSOR = pygame.image.load("images/cursor.png")
STATIONS = []
for sound in range(1, 26):
    num = str(sound // 10) + str(sound % 10)
    if sound <= 8:
        STATIONS.append("SL_new_{}_o_g.mp3".format(num))
        STATIONS.append("SL_new_{}_p_g.mp3".format(num))
    else:
        STATIONS.append("SL_new_{}_o_m.mp3".format(num))
        STATIONS.append("SL_new_{}_p_m.mp3".format(num))

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Красная ветка")
pygame.display.set_icon(pygame.image.load("images/icon.png"))
pygame.mouse.set_visible(0)
pygame.time.set_timer(pygame.USEREVENT, TIMEBETWEENSTATIONS)
clock = pygame.time.Clock()

startMenuSprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def draw_cursor(x, y):
    screen.blit(CURSOR, (x, y))


def settings_screen():
    def draw_buttons():
        # Parameters:             surface,       color,    x,   y, length,height, width, text,   text_color
        exit_button.create_button(screen, (255, 1, 0), 533, 605, 300, 70, 0, "Назад", (0, 0, 0))

    exit_button = Button()
    running_settings_screen = True

    while running_settings_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_settings_screen = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_button.pressed(pygame.mouse.get_pos()):
                        return
        screen.fill(pygame.Color("black"))
        startMenuSprites.draw(screen)
        startMenuSprites.update()
        draw_buttons()
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    def draw_buttons():
        # Parameters:                surface,    color,    x,   y, length,height, width, text,   text_color
        red_line_button.create_button(screen, (255, 1, 0), 326, 77, 715, 117, 0, intro_text[0], (255, 204, 0))
        start_button.create_button(screen, (255, 1, 0), 533, 345, 300, 70, 0, intro_text[1], (0, 0, 0))
        settings_button.create_button(screen, (255, 1, 0), 533, 468, 300, 70, 0, intro_text[2], (0, 0, 0))
        exit_button.create_button(screen, (255, 1, 0), 533, 605, 300, 70, 0, intro_text[3], (0, 0, 0))

    intro_text = ["Красная ветка",
                  "Старт",
                  "Настройки",
                  "Выход"]

    pygame.mixer_music.load("sounds/fon.wav")
    pygame.mixer_music.play(-1)
    click = pygame.mixer.Sound("sounds/click.ogg")
    Fon()
    red_line_button = Button()
    start_button = Button()
    settings_button = Button()
    exit_button = Button()
    draw_buttons()

    running_start_screen = True

    while running_start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_start_screen = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click.play()
                if event.button == 1:
                    if red_line_button.pressed(pygame.mouse.get_pos()):
                        pass
                    elif start_button.pressed(pygame.mouse.get_pos()):
                        return
                    elif settings_button.pressed(pygame.mouse.get_pos()):
                        settings_screen()
                    elif exit_button.pressed(pygame.mouse.get_pos()):
                        terminate()
        screen.fill(pygame.Color((0, 0, 0)))
        startMenuSprites.draw(screen)
        startMenuSprites.update()
        draw_buttons()
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def education_screen():
    pass


class Map:
    pass


class Backpack:
    pass


class Player(pygame.sprite.Sprite):
    pass


class Camera:
    pass


class Subway:
    pass


class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // len(text))
        myFont = pygame.font.Font("Roboto-Black.ttf", font_size)
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
                        return True
        return False


class Fon(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("images/fon.jpg"), (2000, 2000))

    def __init__(self):
        super().__init__(startMenuSprites)
        self.image = Fon.image
        self.rect = Fon.image.get_rect()
        self.rect.left = -634

    def update(self):
        if self.rect.left < 0:
            self.rect.left += 1
        else:
            self.rect.left -= 520


if __name__ == '__main__':
    start_screen()
    pygame.mixer_music.load("sounds/Cyberpunk Moonlight Sonata v2.mp3")
    # pygame.mixer_music.play(-1)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                pass  # Добавить реакцию на нажатия клавиш
            elif event.type == pygame.USEREVENT:
                pass  # Смена станций

        screen.fill(pygame.Color("black"))
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()

        clock.tick(FPS)

    terminate()

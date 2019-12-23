import os
import sys
import pygame
import sqlite3

pygame.init()
pygame.key.set_repeat(100, 70)

FPS = 50
WIDTH = 1366
HEIGHT = 768
STEP = 100
TIMEBETWEENSTATIONS = 150000
CURSOR = pygame.image.load("images/cursor.png")
CLICK = pygame.mixer.Sound("sounds/click.ogg")
STATIONS = []
for sound in range(1, 26):
    num = str(sound // 10) + str(sound % 10)
    if sound <= 8:
        STATIONS.append("SL_new_{}_o_g.mp3".format(num))
        STATIONS.append("SL_new_{}_p_g.mp3".format(num))
    else:
        STATIONS.append("SL_new_{}_o_m.mp3".format(num))
        STATIONS.append("SL_new_{}_p_m.mp3".format(num))

# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Красная ветка")
pygame.display.set_icon(pygame.image.load("images/icon.png"))
pygame.mouse.set_visible(0)
pygame.time.set_timer(pygame.USEREVENT, TIMEBETWEENSTATIONS)
clock = pygame.time.Clock()

start_menu_sprites = pygame.sprite.Group()
all_groups = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wagon_group = pygame.sprite.Group()
icon_group = pygame.sprite.Group()


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
        exit_button.create_button(screen, (255, 1, 0), 81, 44, 300, 70, 0, "Назад", (0, 0, 0))

    exit_button = Button()
    running_settings_screen = True

    while running_settings_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_settings_screen = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                CLICK.play()
                if event.button == 1:
                    if exit_button.pressed(pygame.mouse.get_pos()):
                        return
        screen.fill(pygame.Color("black"))
        start_menu_sprites.draw(screen)
        start_menu_sprites.update()
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
                CLICK.play()
                if event.button == 1:
                    if red_line_button.pressed(pygame.mouse.get_pos()):
                        pass
                    elif start_button.pressed(pygame.mouse.get_pos()):
                        return
                    elif settings_button.pressed(pygame.mouse.get_pos()):
                        settings_screen()
                    elif exit_button.pressed(pygame.mouse.get_pos()):
                        terminate()
        screen.fill(pygame.Color("black"))
        start_menu_sprites.draw(screen)
        start_menu_sprites.update()
        draw_buttons()
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def education_screen():
    running_education_screen = True
    while running_education_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_education_screen = False
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.update("L")
                if event.key == pygame.K_RIGHT:
                    player.update("R")
            elif event.type == pygame.KEYUP:
                player.update("S")
        screen.fill(pygame.Color("black"))
        camera.update(player)

        for sprite in all_groups:
            camera.apply(sprite)
        # if pygame.mouse.get_focused():
        #   draw_cursor(*pygame.mouse.get_pos())
        # all_groups.draw(screen)
        wagon_group.draw(screen)
        icon_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


class Wagon(pygame.sprite.Sprite):
    image_up = pygame.transform.scale(pygame.image.load("images/Крайний вагон (Крыша).png"), (4096, 16))
    image_middle = pygame.transform.scale(pygame.image.load("images/Крайний вагон (Середина).png"), (4096, 630))
    image_down = pygame.transform.scale(pygame.image.load("images/Крайний вагон (Пол).png"), (4096, 9))
    image_cabin = pygame.transform.scale(pygame.image.load("images/Кабинка машиниста.png"), (488, 630))
    image_cabin_rot = pygame.transform.flip(pygame.transform.scale(
        pygame.image.load("images/Кабинка машиниста.png"), (488, 630)), 1, 0)

    def __init__(self, type):
        super().__init__(wagon_group, all_groups)
        if type == "up":
            self.image = Wagon.image_up
            self.rect = self.image.get_rect()
            self.rect.left = -2537
            self.rect.top = 64
        elif type == "middle":
            self.image = Wagon.image_middle
            self.rect = self.image.get_rect()
            self.rect.left = -2727
            self.rect.top = 74
        elif type == "down":
            self.image = Wagon.image_down
            self.rect = self.image.get_rect()
            self.rect.left = -2242
            self.rect.top = 704
        elif type == "cabin":
            self.image = Wagon.image_cabin
            self.rect = self.image.get_rect()
        elif type == "cabin_rot":
            self.image = Wagon.image_cabin_rot
            self.rect = self.image.get_rect()
            self.rect.left = 1364
            self.rect.top = 74
        self.type = type
        self.mask = pygame.mask.from_surface(self.image)


class Map(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("images/map_icon.png"), (128, 128))

    def __init__(self):
        super().__init__(icon_group)
        self.image = Map.image
        self.rect = self.image.get_rect()
        self.rect.left = 1238
        self.rect.top = 0


class Backpack(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("images/backpack.png"), (128, 128))

    def __init__(self):
        super().__init__(icon_group)
        self.image = Backpack.image
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0


class Player(pygame.sprite.Sprite):
    image = pygame.image.load("images/character_malePerson_behindBack.png")

    def __init__(self):
        super().__init__(player_group, all_groups)
        self.image = Player.image
        self.frames_left = []
        self.frames_right = []
        self.frames = [self.image, pygame.image.load("images/character_malePerson_think.png")]
        for i in range(8):
            self.frames_right.append(pygame.image.load(f"images/character_malePerson_walk{i}.png"))
            self.frames_left.append(pygame.transform.flip(pygame.image.load
                                                          (f"images/character_malePerson_walk{i}.png"), 1, 0))

        self.rect = self.image.get_rect()
        self.rect.left = 1080
        self.rect.top = 448
        self.cur_frame = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        who = args[0]
        if who == "L":
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
            self.image = self.frames_left[self.cur_frame]
            player.rect.x -= STEP
            for i in wagon_group:
                if i.type == 'cabin' or i.type == "cabin_rot":
                    if pygame.sprite.collide_mask(self, i):
                        self.image = self.frames[1]
                        player.rect.x += STEP
                        break
        elif who == "R":
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
            self.image = self.frames_right[self.cur_frame]
            player.rect.x += STEP
            for i in wagon_group:
                if i.type == 'cabin' or i.type == "cabin_rot":
                    if pygame.sprite.collide_mask(self, i):
                        self.image = self.frames[1]
                        player.rect.x -= STEP
                        break
        else:
            self.image = self.frames[0]
            self.cur_frame = 0


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


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
        super().__init__(start_menu_sprites)
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
    camera = Camera()
    player = Player()
    wagon_up = Wagon("up")
    wagon_middle = Wagon("middle")
    wagon_down = Wagon("down")
    cabin_last = Wagon("cabin_rot")
    backpack = Backpack()
    map = Map()
    education_screen()
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

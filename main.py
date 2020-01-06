import os
import sys
import time
import pygame
import sqlite3

pygame.init()
pygame.key.set_repeat(100, 70)

FPS = 50
WIDTH = 1366
HEIGHT = 768
STEP = 50
TIMEBETWEENSTATIONS = 150000
TIME = 15000
CURSOR = pygame.image.load("images/icons/cursor.png")
CLICK = pygame.mixer.Sound("sounds/click.ogg")
STATIONS_SOUNDS = []
STATIONS = [("Коммунарка",),
            ("Ольховая",),
            ("Прокшино",),
            ("Филатов Луг",),
            ("Саларьево",),
            ("Румянцево",),
            ("Тропарёво",),
            ("Юго-Западная",),
            ("Проспект Вернадского",),
            ("Университет",),
            ("Воробьёвы горы",),
            ("Спортивная",),
            ("Фрунзенская",),
            ("Парк культуры",),
            ("Кропоткинская",),
            ("Библиотека имени Ленина",),
            ("Охотный Ряд",),
            ("Лубянка",),
            ("Чистые пруды",),
            ("Красные Ворота",),
            ("Комсомольская",),
            ("Красносельская",),
            ("Сокольники",),
            ("Преображенская площадь",),
            ("Черкизовская",),
            ("Бульвар Рокоссовского",)]
directory = "sounds/"
sounds = os.listdir(directory)
for sound in range(len(sounds)):
    if sounds[sound].startswith("SL_new_"):
        STATIONS_SOUNDS.append(sounds[sound])

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Красная ветка")
pygame.display.set_icon(pygame.image.load("images/icons/icon.png"))
pygame.mouse.set_visible(0)
pygame.time.set_timer(pygame.USEREVENT, TIMEBETWEENSTATIONS)
# pygame.time.set_timer(31, TIME)
clock = pygame.time.Clock()

start_menu_sprites = pygame.sprite.Group()
all_groups = pygame.sprite.Group()
player_group = pygame.sprite.Group()
people_group = pygame.sprite.Group()
wagon_group = pygame.sprite.Group()
icon_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()


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


def count_time():
    finish = time.monotonic()
    result_sec = finish - start
    result_min = result_sec / 60
    result_sec = result_sec % 60 * 60
    return int(result_min), int(result_sec) // 100


def draw_cursor(x, y):
    screen.blit(CURSOR, (x, y))


def draw_buttons(obj, c1, c2, c3, x, y, length, height, width, text, text_c1, text_c2, text_c3):
    obj.create_button(screen, (c1, c2, c3), x, y, length, height, width, text, (text_c1, text_c2, text_c3))


def settings_screen():
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
        draw_buttons(exit_button, 255, 1, 0, 81, 44, 300, 70, 0, "Назад", 0, 0, 0)
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
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
        draw_buttons(red_line_button, 255, 1, 0, 326, 77, 715, 117, 0, intro_text[0], 255, 204, 0)
        draw_buttons(start_button, 255, 1, 0, 533, 345, 300, 70, 0, intro_text[1], 0, 0, 0)
        draw_buttons(settings_button, 255, 1, 0, 533, 468, 300, 70, 0, intro_text[2], 0, 0, 0)
        draw_buttons(exit_button, 255, 1, 0, 533, 605, 300, 70, 0, intro_text[3], 0, 0, 0)
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def choice_avatar_screen():
    text = ["Выберите аватар",
            "----->",
            "<-----"]

    pygame.mixer_music.load("sounds/fon.wav")
    pygame.mixer_music.play(-1)
    start_button = Button()
    page_button = Button()
    AVATARS1 = {"bear": (105, 127),
                "chick": (616, 127),
                "cow": (1076, 320),
                "crocodile": (367, 127),
                "dog": (),
                "duck": (),
                "elephant": (),
                "frog": (),
                "giraffe": (),
                "goat": (),
                "gorilla": (),
                "hippo": (),
                "horse": (),
                "monkey": (),
                "moose": (),
                "narwhal": (),
                "owl": (),
                "panda": (),
                "parrot": (),
                "penguin": (),
                "pig": (),
                "rabbit": (),
                "rhino": (),
                "sloth": (),
                "snake": (),
                "walrus": (),
                "whale": (),
                "zebra": ()
                }
    AVATARS2 = {}

    running_choice_screen = True

    while running_choice_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_choice_screen = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                CLICK.play()
                if event.button == 1:
                    if start_button.pressed(pygame.mouse.get_pos()):
                        pass
                    elif page_button.pressed(pygame.mouse.get_pos()):
                        text[1], text[2] = text[2], text[1]
        screen.fill(pygame.Color("black"))
        draw_buttons(start_button, 255, 1, 0, 419, 36, 529, 75, 0, text[0], 255, 204, 0)
        draw_buttons(page_button, 255, 1, 0, 419, 656, 529, 75, 0, text[1], 0, 0, 0)
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


def choice_screen_name():
    text = ["Введите имя",
            "СТАРТ",
            " "]

    pygame.mixer_music.load("sounds/fon.wav")
    pygame.mixer_music.play(-1)
    start_button = Button()
    text_button = Button()
    name_button = Button()

    running_choice_name_screen = True

    while running_choice_name_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                CLICK.play()
                if event.button == 1:
                    if start_button.pressed(pygame.mouse.get_pos()):
                        # Добавить в БД
                        return
            elif event.type == pygame.KEYDOWN:
                if event.unicode == "":
                    text[2] = " "
                elif event.unicode == "\x08":
                    text[2] = text[2][0:-1]
                else:
                    text[2] += event.unicode
        screen.fill(pygame.Color("black"))
        try:
            draw_buttons(name_button, 255, 1, 0, 418, 36, 529, 75, 0, text[0], 255, 204, 0)
            draw_buttons(text_button, 255, 255, 255, 433, 334, 500, 100, 0, text[2], 0, 0, 0)
            draw_buttons(start_button, 255, 1, 0, 418, 656, 529, 75, 0, text[1], 0, 0, 0)
        except ZeroDivisionError:
            text[2] = " "
        if pygame.mouse.get_focused():
            draw_cursor(*pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


class Avatar:
    def __init__(self, name, pos):
        self.image = pygame.transform.load(f"images/avatars/{name}")
        self.rect = self.image.get_rect()
        self.rect.left = pos[0]
        self.rect.top = pos[1]

    def pressed(self, mouse):
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1]:
            return True
        return False


class Mood(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(icon_group)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = 910
        self.rect.top = 680


class Wagon(pygame.sprite.Sprite):
    image_wagon = pygame.image.load("images/Вагон.png")
    image_cabin = pygame.image.load("images/Кабинка машиниста.png")
    image_cabin_rot = pygame.transform.flip(pygame.image.load("images/Кабинка машиниста.png"), 1, 0)
    image_prohod = pygame.image.load("images/Между.png")

    def __init__(self, type, left, top):
        super().__init__(wagon_group, all_groups)
        if type.startswith("wagon"):
            self.image = Wagon.image_wagon
        elif type == "cabin":
            self.image = Wagon.image_cabin
        elif type == "cabin_rot":
            self.image = Wagon.image_cabin_rot
        elif type.startswith("prohod"):
            self.image = Wagon.image_prohod
            self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.type = type
        self.mask = pygame.mask.from_surface(self.image)


class FonWagon(pygame.sprite.Sprite):

    def __init__(self, image, left):
        super().__init__(fon_group, all_groups)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = 0


class Map(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("images/icons/map_icon.png"), (128, 128))

    def __init__(self, current_station):
        super().__init__(icon_group)
        self.image = Map.image
        self.rect = self.image.get_rect()
        self.rect.left = 1238
        self.rect.top = 0
        self.current_station = current_station

    def set_current_station(self, new_current_station):
        self.current_station = new_current_station

    def get_current_station(self):
        return self.current_station


class Board:
    # Конструктор поля
    def __init__(self, width=7, height=7, left=333, top=34, cell_size=100):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.set_view(left, top, cell_size)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # рисование поля
    def render(self):
        pygame.draw.rect(screen, pygame.Color("white"),
                         (self.left, self.top,
                          self.width * self.cell_size, self.height * self.cell_size))
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color("black"),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size, self.cell_size), 1)

    def on_click(self, cell):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y


class Backpack(pygame.sprite.Sprite, Board):
    image = pygame.transform.scale(pygame.image.load("images/icons/backpack.png"), (100, 142))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, icon_group)
        Board.__init__(self)
        self.image = Backpack.image
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
        self.opened = False

    def open(self):
        Board.render(self)


class People(pygame.sprite.Sprite):
    pass


class Player(pygame.sprite.Sprite):
    image = pygame.image.load("images/sprites/character_malePerson_behindBack.png")
    image_think = pygame.image.load("images/sprites/character_malePerson_think.png")
    image_back = pygame.image.load("images/sprites/character_malePerson_back.png")

    def __init__(self):
        super().__init__(player_group, all_groups)
        self.image = Player.image
        self.frames_left = []
        self.frames_right = []
        self.frames_down_left = []
        self.frames_down_right = []
        self.frames = [self.image, Player.image_think, Player.image_back, ]
        for i in range(6):
            self.frames_right.append(pygame.image.load(f"images/sprites/character_malePerson_walk{i}.png"))
            self.frames_left.append(pygame.transform.flip(pygame.image.load
                                                          (f"images/sprites/character_malePerson_walk{i}.png"), 1, 0))

        for i in range(4):
            self.frames_down_right.append(pygame.image.load(f'images/sprites/character_malePerson_crouch{i}.png'))
            self.frames_down_left.append(pygame.transform.flip(pygame.image.load
                                                               (f'images/sprites/character_malePerson_crouch{i}.png'),
                                                               1, 0))

        self.rect = self.image.get_rect()
        self.rect.left = 576
        self.rect.top = 340
        self.cur_frame = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.last = None

    def update(self, *args):
        who = args[0]
        if who == "L":
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
            self.image = self.frames_left[self.cur_frame]
            player.rect.x -= STEP
            for i in wagon_group:
                if i.type == 'cabin' or i.type == "cabin_rot" or (i.type.startswith("prohod") and
                                                                  not flags[int(i.type[-1]) - 1]):
                    if pygame.sprite.collide_mask(self, i):
                        self.image = self.frames[1]
                        player.rect.x += STEP
                        break
        elif who == "R":
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
            self.image = self.frames_right[self.cur_frame]
            player.rect.x += STEP
            for i in wagon_group:
                if i.type == 'cabin' or i.type == "cabin_rot" or (i.type.startswith("prohod") and
                                                                  not flags[int(i.type[-1]) - 1]):
                    if pygame.sprite.collide_mask(self, i):
                        self.image = self.frames[1]
                        player.rect.x -= STEP
                        break
        elif who == "U":
            self.image = self.frames[2]
            self.cur_frame = 2
        elif who == "D":
            if self.cur_frame != 3:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames_down_right)
            if self.last == "R":
                self.image = self.frames_down_right[self.cur_frame]
            elif self.last == "L":
                self.image = self.frames_down_left[self.cur_frame]
            return

        else:
            self.image = self.frames[0]
            self.cur_frame = 0
            return
        self.last = who


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
        self.dy += 170


class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // len(text))
        myFont = pygame.font.Font("font/Roboto-Black.ttf", font_size)
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
        if self.rect.topleft[0] < mouse[0] < self.rect.bottomright[0] and self.rect.topleft[1] < mouse[1] < \
                self.rect.bottomright[1]:
            return True
        return False


class Fon(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load("images/fons/fon.jpg"), (2000, 2000))

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
    # choice_avatar_screen() Не до конца
    # choice_screen_name() Не до конца
    pygame.mixer_music.load("sounds/Cyberpunk Moonlight Sonata v2.mp3")
    flags = [False, False, False, False, False, False]
    menu = False
    menu_text = ["Меню", "Время: ", "Управление", "Назад", "Выход из игры"]
    fon_menu = Button()
    menu_button = Button()
    exit_button = Button()
    back_button = Button()
    time_button = Button()
    control_button = Button()

    camera = Camera()
    player = Player()
    last_wagon = Wagon("wagon7", -3773, 68)
    last_prohod = Wagon("prohod6", -3917, 68)
    last_cabin = Wagon("cabin_rot", 823, 68)

    backpack = Backpack()
    map = Map(STATIONS[0][0])
    # smartphone = Smarthone()
    moods_dict = dict()
    moods = os.listdir("images/mood/")
    for i in range(len(moods)):
        moods_dict[moods[i][4:-4]] = moods[i]
    cur_mood = Mood("images/mood/" + moods_dict["60"])

    directory = "images/fons/Fon_Kommunarka/"
    images = os.listdir(directory)
    left = -32784
    for i in range(len(images)):
        if images[i].startswith("image"):
            FonWagon(directory + images[i], left)
            left += 3415
    num = -2
    # pygame.mixer_music.play(-1)
    running = True
    start = time.monotonic()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.unicode == "\x1b":
                    menu = not menu
                    continue
                if not menu:
                    if event.key == pygame.K_LEFT or event.unicode.lower() == "a":
                        player.update("L")
                    if event.key == pygame.K_RIGHT or event.unicode.lower() == "d":
                        player.update("R")
                    if event.key == pygame.K_UP or event.unicode.lower() == "w":
                        player.update("U")
                    if event.key == pygame.K_DOWN or event.unicode.lower() == "s":
                        player.update("D")
                    if event.unicode.lower() == "m":
                        pass  # Взаимодействие с картой
                    if event.unicode.lower() == "\t":
                        # Взаимодействие с рюкзаком
                        backpack.opened = not backpack.opened
            elif event.type == pygame.KEYUP:
                player.update("S")
            elif event.type == pygame.MOUSEBUTTONDOWN and menu:
                CLICK.play()
                if back_button.pressed(pygame.mouse.get_pos()):
                    menu = False
                elif exit_button.pressed(pygame.mouse.get_pos()):
                    running = False
                    terminate()
            elif event.type == pygame.USEREVENT:
                current_station = pygame.mixer.Sound("sounds/" + STATIONS_SOUNDS[num])
                current_station.play()
                del STATIONS_SOUNDS[num]
                if num == -1:
                    num = -2
                elif num == -2:
                    num = -1

        screen.fill(pygame.Color("black"))
        camera.update(player)

        for sprite in all_groups:
            camera.apply(sprite)
        fon_group.draw(screen)
        wagon_group.draw(screen)
        icon_group.draw(screen)
        player_group.draw(screen)

        if menu:
            draw_buttons(fon_menu, 255, 1, 0, 433, 34, 500, 700, 0, " ", 255, 1, 0)
            draw_buttons(menu_button, 255, 204, 0, 558, 59, 250, 60, 0, menu_text[0], 255, 1, 0)
            draw_buttons(time_button, 255, 255, 255, 518, 150, 330, 100, 0, menu_text[1] + str(count_time()), 0, 0, 0)
            draw_buttons(control_button, 255, 255, 255, 520, 341, 330, 60, 0, menu_text[2], 0, 0, 0)
            draw_buttons(back_button, 255, 255, 255, 519, 461, 330, 60, 0, menu_text[3], 0, 0, 0)
            draw_buttons(exit_button, 255, 255, 255, 518, 649, 330, 60, 0, menu_text[4], 0, 0, 0)
            draw_cursor(*pygame.mouse.get_pos())
        elif backpack.opened:
            backpack.render()
            draw_cursor(*pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(FPS)

    terminate()

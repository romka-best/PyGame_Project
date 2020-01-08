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
dialogs = {
            "wagon1": {
                "myself": [
                    "Ох, отъезжаем, так, мне нужно доехать до бульвара Рокоссовского,\nэто конечная. "
                    "Могу вздремнуть...",
                    "Стой! Здесь подозрительный пакет. Народ! Этот пакет кого-то из вас?", "Ладно, позвоню машинисту.",
                    "Так, мне нужно самому дойти до кабины машиниста. Надо бы\nзаписать в телефон в заметки, "
                    "чтобы не забыть зачем туда пришёл.\nКстати, где он!?",
                    "Ну всё, задачу записал, теперь её надо выполнить пока не доедем\nдо моей станции"],
                "with pair": ["Извините, мне нужно пройти дальше ради вашего же блага!",
                              "Надо придумать, как пройти в следующий вагон..."],
                "with grandfather1": ["Дедушка, не подскажите как сказать той паре, чтобы не стояли\nна проходе",
                                      "Я вам говорю: Не знаете, как сказать той паре, чтобы они не стояли\nна проходе",
                                      "Спасибо!"],
                "with young1": ["Извините, не подскажите, как сказать той паре, что они\nзагораживают проход?",
                                "Так, ну я бы не стал целоваться с любимым человеком при всех.\nХорошо, спасибо!"],
                "with teenagerW1": [
                    "Привет, не подскажешь как убрать ту пару с прохода? Мне очень\nнужно попасть в следующий вагон",
                    "Эмм, я не хотел с тобой целоваться",
                    "!Зачем так унижать людей? Неужели так сложно говорить искренне, но и не грубить?\nПромолчать"]
            }
        }
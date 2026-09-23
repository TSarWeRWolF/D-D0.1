import pygame

from assets import AssetManager
from player import Player
from world import World
from npc import NPC
from battle import Battle


class Game:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (1280, 720)
        )

        pygame.display.set_caption(
            "D&D RPG Prototype"
        )

        self.clock = pygame.time.Clock()
        self.running = True

        # ==========================================
        # Состояние игры
        # ==========================================

        self.location = "city"

        self.dialogue_active = False
        self.quest_active = False
        self.quest_completed = False

        self.gold = 0

        # ==========================================
        # Шрифты
        # ==========================================

        self.font = pygame.font.SysFont(
            "dejavusans",
            24
        )

        self.big_font = pygame.font.SysFont(
            "dejavusans",
            36
        )

        # ==========================================
        # Ассеты
        # ==========================================

        self.assets = AssetManager()
        self.assets.load_images()

        # ==========================================
        # Мир
        # ==========================================

        city_image = self.assets.get(
            "riwerhold"
        )

        self.world = World(
            city_image
        )

        # ==========================================
        # Игрок
        # ==========================================

        hero = self.assets.get(
            "knighthero"
        )

        self.player = Player(
            hero
        )

        # ==========================================
        # Зигфирд
        # ==========================================

        zigfird_image = self.assets.get(
            "zigfird"
        )

        self.zigfird = NPC(
            zigfird_image,
            600,
            250
        )

        # ==========================================
        # Бой
        # ==========================================

        self.battle = Battle(
            self.screen,
            self.assets
        )

        # ==========================================
        # Кнопки
        # ==========================================

        self.tavern_button = pygame.Rect(
            20,
            20,
            260,
            55
        )

        self.city_button = pygame.Rect(
            20,
            20,
            260,
            55
        )

        self.dungeon_button = pygame.Rect(
            20,
            90,
            260,
            55
        )

    # ==========================================
    # Таверна
    # ==========================================

    def enter_tavern(self):

        self.location = "tavern"

        tavern_image = self.assets.get(
            "tavernar"
        )

        self.world = World(
            tavern_image
        )

        self.player.x = 608
        self.player.y = 500

        self.player.target_x = self.player.x
        self.player.target_y = self.player.y

        self.player.rect.x = int(
            self.player.x
        )

        self.player.rect.y = int(
            self.player.y
        )

    # ==========================================
    # Город
    # ==========================================

    def enter_city(self):

        self.location = "city"

        city_image = self.assets.get(
            "riwerhold"
        )

        self.world = World(
            city_image
        )

        self.player.x = 608
        self.player.y = 328

        self.player.target_x = self.player.x
        self.player.target_y = self.player.y

        self.player.rect.x = int(
            self.player.x
        )

        self.player.rect.y = int(
            self.player.y
        )

    # ==========================================
    # Подземелье
    # ==========================================

    def enter_dungeon(self):

        self.location = "dungeon"

        dungeon_image = self.assets.get(
            "maindiomand"
        )

        self.world = World(
            dungeon_image
        )

        self.battle.start()

    # ==========================================
    # Диалог
    # ==========================================

    def draw_dialogue(self):

        dialogue_box = pygame.Rect(
            50,
            500,
            1180,
            170
        )

        pygame.draw.rect(
            self.screen,
            (20, 20, 20),
            dialogue_box
        )

        pygame.draw.rect(
            self.screen,
            (180, 180, 180),
            dialogue_box,
            3
        )

        name_text = self.big_font.render(
            "Зигфирд",
            True,
            (255, 220, 100)
        )

        self.screen.blit(
            name_text,
            (80, 525)
        )

        text1 = self.font.render(
            "Кароче, хочешь подзаработать?",
            True,
            (255, 255, 255)
        )

        text2 = self.font.render(
            "Так вот, пойди и убей драугров.",
            True,
            (255, 255, 255)
        )

        text3 = self.font.render(
            "И я тебе дам 100 золотых.",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            text1,
            (80, 565)
        )

        self.screen.blit(
            text2,
            (80, 600)
        )

        self.screen.blit(
            text3,
            (80, 635)
        )

        accept_button = pygame.Rect(
            950,
            575,
            230,
            60
        )

        pygame.draw.rect(
            self.screen,
            (70, 120, 70),
            accept_button
        )

        button_text = self.font.render(
            "Взять задание",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            button_text,
            (
                accept_button.x + 25,
                accept_button.y + 14
            )
        )

    # ==========================================
    # События
    # ==========================================

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button != 1:
                    continue

                mouse_pos = event.pos

                # ==================================
                # ГОРОД
                # ==================================

                if self.location == "city":

                    # Таверна
                    if self.tavern_button.collidepoint(
                        mouse_pos
                    ):

                        self.enter_tavern()

                    # Подземелье
                    elif (
                        self.quest_active
                        and
                        self.dungeon_button.collidepoint(
                            mouse_pos
                        )
                    ):

                        self.enter_dungeon()

                    else:

                        self.player.handle_click(
                            mouse_pos
                        )

                # ==================================
                # ТАВЕРНА
                # ==================================

                elif self.location == "tavern":

                    # Диалог
                    if self.dialogue_active:

                        # ==========================================
                        # КВЕСТ УЖЕ ВЫПОЛНЕН
                        # ==========================================

                        if self.quest_completed:

                            self.gold += 100

                            self.quest_completed = False
                            self.quest_active = False
                            self.dialogue_active = False

                            print("Награда получена: +100 золота")
                            print("Всего золота:", self.gold)

                        # ==========================================
                        # КВЕСТ ЕЩЁ НЕ ВЫПОЛНЕН
                        # ==========================================

                        else:

                            accept_button = pygame.Rect(
                                950,
                                575,
                                230,
                                60
                            )

                            if accept_button.collidepoint(
                                    mouse_pos
                            ):
                                self.quest_active = True
                                self.dialogue_active = False

                    else:

                        # Вернуться в город
                        if self.city_button.collidepoint(
                                mouse_pos
                        ):

                            self.enter_city()

                        # Нажатие на Зигфирда
                        elif self.zigfird.rect.collidepoint(
                                mouse_pos
                        ):

                            self.dialogue_active = True

                        else:

                            self.player.handle_click(
                                mouse_pos
                            )
                # ==================================
                # ПОДЗЕМЕЛЬЕ
                # ==================================

                # ==================================
                # ПОДЗЕМЕЛЬЕ
                # ==================================

                elif self.location == "dungeon":

                    if self.battle.finished:

                        return_button = pygame.Rect(
                            900,
                            620,
                            300,
                            60
                        )

                        if return_button.collidepoint(
                                mouse_pos
                        ):
                            # Квест выполнен
                            self.quest_completed = True

                            # Квест больше не активен
                            self.quest_active = False

                            # Возвращаемся в город
                            self.enter_city()

                            print("КВЕСТ ВЫПОЛНЕН!")
                            print(
                                "quest_completed =",
                                self.quest_completed
                            )

                    else:

                        self.battle.handle_click(
                            mouse_pos
                        )
    # ==========================================
    # Рисование
    # ==========================================

    def draw(self):

        # ==========================================
        # ПОДЗЕМЕЛЬЕ
        # ==========================================

        if self.location == "dungeon":

            self.battle.draw()

            # После победы
            if self.battle.finished:

                return_button = pygame.Rect(
                    900,
                    620,
                    300,
                    60
                )

                pygame.draw.rect(
                    self.screen,
                    (70, 120, 70),
                    return_button
                )

                text = self.font.render(
                    "Вернуться в город",
                    True,
                    (255, 255, 255)
                )

                self.screen.blit(
                    text,
                    (
                        925,
                        637
                    )
                )

            return

        # ==========================================
        # Обычная локация
        # ==========================================

        self.screen.fill(
            (0, 0, 0)
        )

        self.world.draw(
            self.screen
        )

        self.player.draw(
            self.screen
        )

        # ==========================================
        # ГОРОД
        # ==========================================

        if self.location == "city":

            pygame.draw.rect(
                self.screen,
                (60, 90, 140),
                self.tavern_button
            )

            text = self.font.render(
                "Переместиться в таверну",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                text,
                (
                    32,
                    33
                )
            )

            # Подземелье доступно только после квеста
            if self.quest_active:

                pygame.draw.rect(
                    self.screen,
                    (90, 70, 110),
                    self.dungeon_button
                )

                dungeon_text = self.font.render(
                    "Отправиться в подземелье",
                    True,
                    (255, 255, 255)
                )

                self.screen.blit(
                    dungeon_text,
                    (
                        32,
                        103
                    )
                )

        # ==========================================
        # ТАВЕРНА
        # ==========================================

        elif self.location == "tavern":

            self.zigfird.draw(
                self.screen
            )

            # Кнопка обратно
            pygame.draw.rect(
                self.screen,
                (80, 80, 100),
                self.city_button
            )

            city_text = self.font.render(
                "Вернуться в город",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                city_text,
                (
                    42,
                    33
                )
            )

            if not self.dialogue_active:

                hint = self.font.render(
                    "Нажми на Зигфирда",
                    True,
                    (255, 255, 255)
                )

                self.screen.blit(
                    hint,
                    (20, 670)
                )

        # ==========================================
        # Диалог
        # ==========================================

        if self.dialogue_active:

            self.draw_dialogue()

        # ==========================================
        # Квест
        # ==========================================

        if self.quest_active:

            quest_text = self.font.render(
                "Задание: убить 4 драугров | Награда: 100 золота",
                True,
                (255, 220, 100)
            )

            self.screen.blit(
                quest_text,
                (20, 670)
            )

        # ==========================================
        # Золото
        # ==========================================

        gold_text = self.font.render(
            f"Золото: {self.gold}",
            True,
            (255, 220, 100)
        )

        self.screen.blit(
            gold_text,
            (1050, 20)
        )

    # ==========================================
    # Главный цикл
    # ==========================================

    def run(self):

        while self.running:

            self.handle_events()

            # Движение героя
            if (
                self.location != "dungeon"
                and not self.dialogue_active
            ):

                self.player.update()

            # ======================================
            # После победы — обратно в город
            # ======================================

            if (
                self.location == "dungeon"
                and self.battle.finished
            ):

                # Пока только ожидаем нажатия кнопки
                pass

            self.draw()

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
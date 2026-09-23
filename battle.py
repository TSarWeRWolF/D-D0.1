import pygame
import time


class Battle:

    def __init__(self, screen, assets):

        self.screen = screen
        self.assets = assets

        # ==========================================
        # Состояние боя
        # ==========================================

        self.active = False
        self.finished = False
        self.player_turn = True

        # Выбранное действие
        self.selected_action = None

        # ==========================================
        # Игрок
        # ==========================================

        self.player_max_hp = 100
        self.player_hp = 100

        # ==========================================
        # Драугры
        # ==========================================

        self.draugrs = [

            {
                "name": "Драугр 1",
                "hp": 100,
                "max_hp": 100,
                "x": 250,
                "y": 150,
                "alive": True
            },

            {
                "name": "Драугр 2",
                "hp": 100,
                "max_hp": 100,
                "x": 800,
                "y": 150,
                "alive": True
            },

            {
                "name": "Драугр 3",
                "hp": 100,
                "max_hp": 100,
                "x": 250,
                "y": 380,
                "alive": True
            },

            {
                "name": "Драугр 4",
                "hp": 100,
                "max_hp": 100,
                "x": 800,
                "y": 380,
                "alive": True
            }
        ]

        # ==========================================
        # Перезарядки
        # ==========================================

        self.magic_cooldown = 20
        self.heal_cooldown = 35

        self.last_magic_time = -999
        self.last_heal_time = -999

        # ==========================================
        # Сообщение
        # ==========================================

        self.message = (
            "Ваш ход. Выберите действие."
        )

        # ==========================================
        # Шрифты
        # ==========================================

        self.font = pygame.font.SysFont(
            "dejavusans",
            24
        )

        self.big_font = pygame.font.SysFont(
            "dejavusans",
            32
        )

        # ==========================================
        # Картинки
        # ==========================================

        self.dungeon_image = self.assets.get(
            "maindiomand"
        )

        self.draugr_image = self.assets.get(
            "draugr"
        )

        if self.draugr_image is not None:

            self.draugr_image = pygame.transform.scale(
                self.draugr_image,
                (100, 100)
            )

    # ==========================================
    # Начало боя
    # ==========================================

    def start(self):

        self.active = True
        self.finished = False
        self.player_turn = True

        self.selected_action = None

        self.current_enemy = 0

        self.player_hp = 100

        for draugr in self.draugrs:
            draugr["hp"] = 100
            draugr["alive"] = True

        self.last_magic_time = -999
        self.last_heal_time = -999

        self.message = (
            "Ваш ход. Выберите действие."
        )

    # ==========================================
    # Проверка победы
    # ==========================================

    def check_victory(self):

        for draugr in self.draugrs:

            if draugr["alive"]:

                return False

        self.finished = True
        self.selected_action = None

        self.message = (
            "Все драугры повержены!"
        )

        return True

    # ==========================================
    # Проверка смерти игрока
    # ==========================================

    def check_player_death(self):

        if self.player_hp <= 0:

            self.player_hp = 0
            self.active = False
            self.selected_action = None

            self.message = (
                "Вы погибли..."
            )

            return True

        return False

    # ==========================================
    # Поиск драугра
    # ==========================================

    def get_draugr_at(self, mouse_pos):

        mouse_x, mouse_y = mouse_pos

        for index, draugr in enumerate(
            self.draugrs
        ):

            if not draugr["alive"]:
                continue

            rect = pygame.Rect(
                draugr["x"],
                draugr["y"],
                100,
                100
            )

            if rect.collidepoint(
                mouse_x,
                mouse_y
            ):

                return index

        return None

    # ==========================================
    # Атака мечом
    # ==========================================

    def sword_attack(self, target_index):

        if not self.player_turn:
            return

        draugr = self.draugrs[target_index]

        draugr["hp"] -= 20

        self.message = (
            f"Вы ударили "
            f"{draugr['name']} мечом! "
            f"-20 HP"
        )

        if draugr["hp"] <= 0:

            draugr["hp"] = 0
            draugr["alive"] = False

            self.message = (
                f"{draugr['name']} "
                f"повержен!"
            )

        self.selected_action = None

        if self.check_victory():
            return

        self.end_player_turn()

    # ==========================================
    # Магическая атака
    # ==========================================

    def magic_attack(self, target_index):

        if not self.player_turn:
            return

        current_time = time.time()

        if (
            current_time
            - self.last_magic_time
            < self.magic_cooldown
        ):

            remaining = int(
                self.magic_cooldown
                - (
                    current_time
                    - self.last_magic_time
                )
            )

            self.message = (
                "Магия перезаряжается: "
                f"{remaining} сек."
            )

            self.selected_action = None

            return

        draugr = self.draugrs[target_index]

        draugr["hp"] -= 45

        self.last_magic_time = current_time

        self.message = (
            f"Вы использовали магию! "
            f"{draugr['name']} -45 HP"
        )

        if draugr["hp"] <= 0:

            draugr["hp"] = 0
            draugr["alive"] = False

            self.message = (
                f"{draugr['name']} "
                f"уничтожен магией!"
            )

        self.selected_action = None

        if self.check_victory():
            return

        self.end_player_turn()

    # ==========================================
    # Исцеление
    # ==========================================

    def heal(self):

        if not self.player_turn:
            return

        current_time = time.time()

        if (
            current_time
            - self.last_heal_time
            < self.heal_cooldown
        ):

            remaining = int(
                self.heal_cooldown
                - (
                    current_time
                    - self.last_heal_time
                )
            )

            self.message = (
                "Исцеление "
                "перезаряжается: "
                f"{remaining} сек."
            )

            return

        old_hp = self.player_hp

        self.player_hp += 30

        if self.player_hp > self.player_max_hp:

            self.player_hp = self.player_max_hp

        healed = self.player_hp - old_hp

        self.last_heal_time = current_time

        self.message = (
            f"Вы восстановили "
            f"{healed} HP."
        )

        self.selected_action = None

        self.end_player_turn()

    # ==========================================
    # Конец хода игрока
    # ==========================================

    def end_player_turn(self):

        self.player_turn = False

        self.enemy_turns()

    # ==========================================
    # Ход драугров
    # ==========================================

    def enemy_turns(self):

        # Находим следующего живого драугра
        # по очереди

        living_draugrs = []

        for index, draugr in enumerate(self.draugrs):

            if draugr["alive"]:
                living_draugrs.append(index)

        # Если живых драугров нет
        if not living_draugrs:
            self.check_victory()
            return

        # Если текущий драугр ещё не выбран
        if not hasattr(self, "current_enemy"):
            self.current_enemy = 0

        # Если индекс вышел за количество живых
        if self.current_enemy >= len(living_draugrs):
            self.current_enemy = 0

        # Берём одного драугра
        enemy_index = living_draugrs[
            self.current_enemy
        ]

        draugr = self.draugrs[
            enemy_index
        ]

        # Атака одного драугра
        self.player_hp -= 10

        if self.player_hp < 0:
            self.player_hp = 0

        self.message = (
            f"{draugr['name']} "
            f"атакует! -10 HP"
        )

        # Проверяем смерть игрока

        if self.check_player_death():
            return

        # Следующий драугр
        self.current_enemy += 1

        # Возвращаем ход игроку

        self.player_turn = True

        self.message = (
            "Ваш ход. "
            "Выберите действие."
        )

    # ==========================================
    # Обработка мыши
    # ==========================================

    def handle_click(self, mouse_pos):

        if not self.active:
            return

        if self.finished:
            return

        # ======================================
        # Кнопки действий
        # ======================================

        sword_button = pygame.Rect(
            20,
            620,
            230,
            60
        )

        magic_button = pygame.Rect(
            270,
            620,
            230,
            60
        )

        heal_button = pygame.Rect(
            520,
            620,
            230,
            60
        )

        # ======================================
        # Выбор меча
        # ======================================

        if sword_button.collidepoint(mouse_pos):

            if self.player_turn:

                self.selected_action = "sword"

                self.message = (
                    "Вы выбрали меч. "
                    "Нажмите на драугра."
                )

            return

        # ======================================
        # Выбор магии
        # ======================================

        if magic_button.collidepoint(mouse_pos):

            if self.player_turn:

                current_time = time.time()

                if (
                    current_time
                    - self.last_magic_time
                    < self.magic_cooldown
                ):

                    remaining = int(
                        self.magic_cooldown
                        - (
                            current_time
                            - self.last_magic_time
                        )
                    )

                    self.message = (
                        "Магия перезаряжается: "
                        f"{remaining} сек."
                    )

                    return

                self.selected_action = "magic"

                self.message = (
                    "Вы выбрали магию. "
                    "Нажмите на драугра."
                )

            return

        # ======================================
        # Исцеление
        # ======================================

        if heal_button.collidepoint(mouse_pos):

            if self.player_turn:

                self.heal()

            return

        # ======================================
        # Нажатие на драугра
        # ======================================

        target = self.get_draugr_at(
            mouse_pos
        )

        if target is None:

            return

        # ======================================
        # Выполняем выбранное действие
        # ======================================

        if self.selected_action == "sword":

            self.sword_attack(target)

        elif self.selected_action == "magic":

            self.magic_attack(target)

        else:

            self.message = (
                "Сначала выберите "
                "меч или магию."
            )

    # ==========================================
    # Отрисовка
    # ==========================================

    def draw(self):

        # ======================================
        # Фон подземелья
        # ======================================

        if self.dungeon_image is not None:

            dungeon_background = pygame.transform.scale(
                self.dungeon_image,
                (1280, 720)
            )

            self.screen.blit(
                dungeon_background,
                (0, 0)
            )

        else:

            self.screen.fill(
                (30, 25, 20)
            )

        # ======================================
        # Заголовок
        # ======================================

        title = self.big_font.render(
            "ПОДЗЕМЕЛЬЕ — БОЙ",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (20, 20)
        )

        # ======================================
        # HP игрока
        # ======================================

        player_text = self.font.render(
            f"Герой: "
            f"{self.player_hp} / "
            f"{self.player_max_hp} HP",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            player_text,
            (20, 70)
        )

        # ======================================
        # Драугры
        # ======================================

        for draugr in self.draugrs:

            if not draugr["alive"]:
                continue

            if self.draugr_image is not None:

                self.screen.blit(
                    self.draugr_image,
                    (
                        draugr["x"],
                        draugr["y"]
                    )
                )

            name = self.font.render(
                draugr["name"],
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                name,
                (
                    draugr["x"],
                    draugr["y"] - 30
                )
            )

            hp = self.font.render(
                f"HP: "
                f"{draugr['hp']} / 100",
                True,
                (255, 100, 100)
            )

            self.screen.blit(
                hp,
                (
                    draugr["x"],
                    draugr["y"] + 105
                )
            )

        # ======================================
        # Сообщение
        # ======================================

        message = self.font.render(
            self.message,
            True,
            (255, 220, 100)
        )

        self.screen.blit(
            message,
            (20, 570)
        )

        # ======================================
        # Кнопка меча
        # ======================================

        sword_color = (
            (150, 100, 60)
            if self.selected_action == "sword"
            else (100, 70, 50)
        )

        pygame.draw.rect(
            self.screen,
            sword_color,
            (20, 620, 230, 60)
        )

        sword_text = self.font.render(
            "1 — Атака мечем -20",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            sword_text,
            (35, 637)
        )

        # ======================================
        # Кнопка магии
        # ======================================

        magic_color = (
            (100, 100, 190)
            if self.selected_action == "magic"
            else (70, 70, 140)
        )

        pygame.draw.rect(
            self.screen,
            magic_color,
            (270, 620, 230, 60)
        )

        magic_text = self.font.render(
            "2 — Атака магией -45",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            magic_text,
            (285, 637)
        )

        # ======================================
        # Кнопка лечения
        # ======================================

        pygame.draw.rect(
            self.screen,
            (60, 120, 70),
            (520, 620, 230, 60)
        )

        heal_text = self.font.render(
            "3 — Исцеление +30",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            heal_text,
            (535, 637)
        )
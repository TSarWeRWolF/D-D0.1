import pygame
import math


class Player:

    def __init__(self, image):

        self.image = image

        # Размер героя
        self.width = 64
        self.height = 64

        if self.image is not None:
            self.image = pygame.transform.scale(
                self.image,
                (self.width, self.height)
            )

        # Начальная позиция
        self.x = 608
        self.y = 328

        # Скорость движения
        self.speed = 4

        # Точка назначения
        self.target_x = self.x
        self.target_y = self.y

        # Прямоугольник героя
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def handle_click(self, mouse_pos):

        # Получаем координаты клика
        self.target_x = mouse_pos[0] - self.width // 2
        self.target_y = mouse_pos[1] - self.height // 2

    def update(self):

        # Разница между героем и целью
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        # Расстояние до цели
        distance = math.sqrt(
            dx * dx + dy * dy
        )

        # Если достаточно близко — останавливаемся
        if distance < self.speed:

            self.x = self.target_x
            self.y = self.target_y

        else:

            # Нормализуем направление
            direction_x = dx / distance
            direction_y = dy / distance

            # Двигаем героя
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

        # Обновляем Rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):

        if self.image is not None:

            screen.blit(
                self.image,
                (int(self.x), int(self.y))
            )
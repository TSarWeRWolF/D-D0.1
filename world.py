import pygame


class World:

    def __init__(self, image):

        self.image = image

        # Невидимые стены карты
        # Формат:
        # pygame.Rect(x, y, width, height)

        self.walls = [

            # Пример верхней стены
            pygame.Rect(0, 0, 1280, 20),

            # Пример левой стены
            pygame.Rect(0, 0, 20, 720),

            # Пример правой стены
            pygame.Rect(1260, 0, 20, 720),

            # Пример нижней стены
            pygame.Rect(0, 700, 1280, 20),

        ]

    def draw(self, screen):

        if self.image is not None:
            screen.blit(self.image, (0, 0))
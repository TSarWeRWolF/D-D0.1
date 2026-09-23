import pygame


class NPC:

    def __init__(self, image, x, y):

        self.image = image

        self.x = x
        self.y = y

        # Размер картинки NPC
        if self.image is not None:

            self.rect = self.image.get_rect(
                topleft=(self.x, self.y)
            )

        else:

            self.rect = pygame.Rect(
                self.x,
                self.y,
                100,
                100
            )

    def draw(self, screen):

        if self.image is not None:

            screen.blit(
                self.image,
                (self.x, self.y)
            )
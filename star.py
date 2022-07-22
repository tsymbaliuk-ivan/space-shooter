import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """A class to represent a single star in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the atar and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the star image and get its rect.
        self.image = pygame.image.load('images/star.png')
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()

        #  сохраняем прямоугольник экрана
        self.screen_rect = screen.get_rect()

        # Каждая новая звезда появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store a decimal value for the ship's center.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # star speed
        self.star_speed_factor = ai_settings.star_speed_factor

    def blitme(self):
        """Draw the ship at its current location."""
        #  выводитм изображение на экран
        # в позиции, заданной self.rect.
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the star down the screen."""
        self.y += self.star_speed_factor  # Update the decimal position of the bullet
        self.rect.y = self.y  # Update the rect position.

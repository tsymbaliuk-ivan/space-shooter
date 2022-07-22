import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """A class to represent explosion."""

    def __init__(self, ai_settings, screen):
        """Initialize the explosion and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/burst.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        #  сохраняем прямоугольник экрана
        self.screen_rect = screen.get_rect()

        # Каждый новый взрыв появляется в левом верхнем углу экрана.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store a decimal value for the ship's center.
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw explosion at its current location."""
        self.screen.blit(self.image, self.rect)
import pygame


class Ship:

    def __init__(self,ai_settings, screen):
        """Initialize the ship and set its starting position."""
        self.screen = screen
        self.ai_settings = ai_settings
        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.image.set_colorkey((230, 230, 230))
        self.rect = self.image.get_rect()
        #  сохраняем прямоугольник экрана
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        # затем присваиваем значение атрибута centerx прямоугольника экрана к
        # атрибуту centerx прямоугольника корабля
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""

        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center



    def blitme(self):
        """Draw the ship at its current location."""
        #  выводитм изображение на экран
        # в позиции, заданной self.rect.
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.center = self.screen_rect.centerx
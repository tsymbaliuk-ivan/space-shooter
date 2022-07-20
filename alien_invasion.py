import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group
from button import Button

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    # ai_settings is instance of Settings
    ai_settings = Settings()
    # Create a screen
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, "Play")

    # Создание экземпляра для хранения игровой статистики.
    stats = GameStats(ai_settings)

    # Make a ship
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship,  aliens)

    while True:

        # проверяет ввод, полученный от игрока
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:
            # Позиция корабля будет обновляться после проверки событий клавиатуры,
            ship.update()
            # и всех выпущенных пуль
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings,stats,screen, ship, aliens, bullets)
        # отрисовка
        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button)


run_game()

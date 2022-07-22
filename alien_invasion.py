import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group
from button import Button
from scoreboard import Scoreboard

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

    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    scoreboard_ = Scoreboard(ai_settings, screen, stats)


    # Make a ship
    ship = Ship(ai_settings, screen)

    # Make a groups to store bullets, aliens, stars
    stars = Group()
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create the fleet of stars.
    gf.create_stars(ai_settings, screen, stars)

    while True:
        gf.check_events(ai_settings, screen, stats,scoreboard_, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_stars(stars, ai_settings)
            gf.update_bullets(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)

            if len(stars) <= 20:
                gf.create_stars(ai_settings, screen, stars)

        gf.update_screen(ai_settings, screen, stats,scoreboard_, ship, bullets, aliens, play_button, stars)


run_game()

import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    scoreboard_ = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    stars = Group()
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create the fleet of stars.
    gf.create_stars(ai_settings, screen, stars)

    pygame.mixer.music.load("sounds/Wave_Saver_Humbot.mp3")
    pygame.mixer.music.play(-1)

    shot_sound = pygame.mixer.Sound("sounds/shot.ogg")
    shot_sound.set_volume(0.5)

    explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")
    explosion_sound.set_volume(0.5)



    while True:

        gf.check_events(ai_settings, screen, stats, scoreboard_, play_button, ship, aliens, bullets, shot_sound )

        if stats.game_active:
            ship.update()
            gf.update_stars(stars, ai_settings)
            gf.update_bullets(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets, explosion_sound)
            gf.update_aliens(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets)


            if len(stars) <= 20:
                gf.create_stars(ai_settings, screen, stars)

        gf.update_screen(ai_settings, screen, stats, scoreboard_, ship, bullets, aliens, play_button, stars)


run_game()

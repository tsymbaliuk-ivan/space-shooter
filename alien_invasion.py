import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group
from button import Button
from scoreboard import Scoreboard
from sounds import Sounds

def run_game():
    """main function"""
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
    sounds = Sounds()

    explosion = Group()
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create the fleet of stars.
    gf.create_stars(ai_settings, screen, stars)

    # Create main sounds track
    gf.create_sound_track(sounds)

    #_______________________________________________________

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, size):
            pygame.sprite.Sprite.__init__(self)
            self.size = size
            self.image = explosion_anim[self.size][0]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(explosion_anim[self.size]):
                    self.kill()
                else:
                    center = self.rect.center
                    self.image = explosion_anim[self.size][self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center

    explosion_anim = {}
    explosion_anim['lg'] = []
    explosion_anim['sm'] = []
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load('/'.join(('explosions', filename))).convert()
        img.set_colorkey((0,0,0))
        img_lg = pygame.transform.scale(img, (75, 75))
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        explosion_anim['sm'].append(img_sm)

    while True:

        gf.check_events(ai_settings, screen, stats, scoreboard_, play_button, ship, aliens, bullets, sounds)
        if stats.game_active:
            ship.update()
            gf.update_stars(stars, ai_settings, screen)
            gf.update_bullets(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets, sounds)
            gf.update_aliens(ai_settings, screen, stats, scoreboard_, ship, aliens, bullets)


        gf.update_screen(ai_settings, screen, stats, scoreboard_, ship, bullets, aliens, play_button, stars)

        explosion.update()
        # проверьте, не попала ли пуля в моб
        hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for hit in hits:
            expl = Explosion(hit.rect.center, 'lg')
            explosion.add(expl)
        explosion.draw(screen)
        pygame.display.flip()





run_game()

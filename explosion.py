import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion_anim = dict()
        self.explosion_anim['lg'] = []
        self.explosion_anim['sm'] = []
        for i in range(9):
            self.filename = 'regularExplosion0{}.png'.format(i)
            self.img = pygame.image.load('/'.join(('explosions', self.filename))).convert()
            self.img.set_colorkey((0, 0, 0))
            self.img_lg = pygame.transform.scale(self.img, (75, 75))
            self.explosion_anim['lg'].append(self.img_lg)
            self.img_sm = pygame.transform.scale(self.img, (32, 32))
            self.explosion_anim['sm'].append(self.img_sm)
        self.image = self.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.now = pygame.time.get_ticks()

    def update(self):

        if self.now - self.last_update > self.frame_rate:
            self.last_update = self.now
            self.frame += 1
            if self.frame == len(self.explosion_anim[self.size]):
                self.kill()
            else:
                self.center = self.rect.center
                self.image = self.explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = self.center


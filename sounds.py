import pygame


class Sounds:
    """A class to represent a all sounds"""
    def __int__(self):
        """Initialize the sounds settings."""
        self.initialize_settings()


    def initialize_settings(self):
        """Initialize sounds"""
        self.main_sound = pygame.mixer.music.load("sounds/Wave_Saver_Humbot.mp3")
        self.shot_sound = pygame.mixer.Sound("sounds/shot.ogg")
        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")
        self.play = pygame.mixer.music.play(-1)
        self.shot_sound.set_volume(0.25)
        self.explosion_sound.set_volume(0.15)

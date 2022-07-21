class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings.
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.star_speed_factor = 0.1

        # ship settings.
        self.ship_speed_factor = 0.5
        self.ship_limit = 3



        # Bullet settings.
        self.bullet_speed_factor = 0.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 247, 145, 13
        self.bullets_allowed = 3

        # Alien
        self.alien_speed_factor = 0.05
        self.fleet_drop_speed = 10


        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

        # Темп ускорения игры
        # self.speedup_scale = 1
        # инициализирует значения атрибутов, которые
        # должны изменяться в ходе игры
        # self.initialize_dynamic_settings()
        self.alien_points = 1
    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        # self.ship_speed_factor = 1.5
        # self.bullet_speed_factor = 3
        # self.alien_speed_factor = 1
        # self.fleet_direction = 1


    # def increase_speed(self):
    #     """Увеличивает настройки скорости."""
    #     self.ship_speed_factor *= self.speedup_scale
    #     self.bullet_speed_factor *= self.speedup_scale
    #     self.alien_speed_factor *= self.speedup_scale

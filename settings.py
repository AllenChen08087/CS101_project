class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        #self.bullets_allowed = 3
        self.bullets_cooldown = 900

        # Alien settings.
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #ufo settings
        self.ufo_speed = 2.0

        #ufo bullet settings
        self.ufo_bullet_speed = 5
        self.ufo_bullet_width = 10
        self.ufo_bullet_height = 15
        self.ufo_bullet_color = (255, 60, 60)
        self.ufo_bullets_cooldown = 800

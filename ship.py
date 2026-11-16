import pygame
from pygame.sprite import Sprite

#Ship inherits from Sprite so both ships can go in one group and use kill()/alive()
class Ship(Sprite):
    """A class to manage one player's ship."""

    #everything that's different between the two players gets passed in,
    #so we can make as many ships as we want from the same class
    def __init__(self, ai_game, image_files, controls, starting_x_position):
        """Initialize the ship and set its starting position."""
        super().__init__() #runs Sprite's __init__ too, needed or adding the ship to a group crashes
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.controls = controls #Player Keys
        self.starting_x_position = starting_x_position #Where ship starts on the screen
        self.ships_left = self.settings.ship_limit #Ship's life, each ship tracks its own instead of GameStats
        self.last_shot_time = 0 #Ship's cooldown, time of this ship's last shot in milliseconds

        # Load the ship image and get its rect.
        self.image = pygame.image.load(image_files)
        self.rect = self.image.get_rect()

        #We move ship to their own starting spot instead of the center

        # Movement flags; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False

        self.center_ship() #called last since it needs self.rect and starting_x_position

    def center_ship(self):
        """Move the ship back to its own starting spot at the bottom of the screen."""
        #midbottom is the middle of the bottom edge of the rect
        self.rect.midbottom = (self.starting_x_position, self.screen_rect.bottom)
        #rect can only hold whole numbers but ship_speed is 1.5, so the exact position is kept as a float
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
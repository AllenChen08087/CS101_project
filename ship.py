import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game, image_files, controls, starting_x_position):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.controls = controls #Player Keys
        self.starting_x_position = starting_x_position #Where ship starts on the screen
        self.ships_left = self.settings.ship_limit #Ship's life
        self.last_shot_time = 0 #Ship's cooldown

        # Load the ship image and get its rect.
        self.image = pygame.image.load(image_files)
        self.rect = self.image.get_rect()

        #We move ship to their own starting spot instead of the center

        # Movement flags; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False

        self.center_ship()

    def center_ship(self):
        self.rect.midbottom = (self.starting_x_position, self.screen_rect.bottom)
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
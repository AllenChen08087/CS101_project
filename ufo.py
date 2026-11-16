import pygame


class Ufo:
    """A class to manage the ufo"""

    def __init__(self, ai_game):
        """Initialize the ufo and set its starting position."""

        #test1 if the ufo appears at the middle top of the screen at the start of the game
        #expected result: a ufo at the middle top of the screen at the start of the game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


        # Load the ufo image and get its rect.
        self.image = pygame.image.load('images/skull_in_a_ufo_spacecraft.bmp')
        self.image = pygame.transform.scale(self.image, (85, 60))

        self.rect = self.image.get_rect()

        # Start the ufo at the bottom center of the screen.
        self.rect.midtop = self.screen_rect.midtop

        # Store a float for the ufo's horizontal position.
        self.x = float(self.rect.x)

        #Initialize the direction ufo is moving toward (right)
        self.direction = 1

        # Movement flags; start with a ufo that's not moving.
        self.moving_right = False
        self.moving_left = False

    def center_ufo(self):
        """Center the ufo on the screen."""
        self.rect.midtop = self.screen_rect.midtop
        self.x = float(self.rect.x)

    def update(self):
        """Update the ufo's position based on the speed in the setting."""

        self.x += self.settings.ufo_speed * self.direction
        self.rect.x = self.x

        #changing direction of the ufo once hitting the boundary
        #test2: test if the ufo is moving left and right at constant speed indicated in the setting before making it firing bullets
        #expected result: the ufo starts in the middle top of the screen at the beginning of the game, first moves to the right at a constant speed
        #                 until hitting the boundary, then moves to the left until hitting the boundary, and so on.
        if self.rect.right >= self.screen_rect.right:
            self.direction *= -1
        if self.rect.left <= self.screen_rect.left:
            self.direction *= -1


        # Update rect object from self.x.
        self.rect.x = self.x


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
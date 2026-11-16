import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from ufo import Ufo
from ufo_bullet import UfoBullet


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        #Player controls
        red_controls = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "fire": pygame.K_r
        }
        blue_controls = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "fire": pygame.K_SPACE
        }
        width = self.settings.screen_width
        #Creating the 2 ships
        self.ships = pygame.sprite.Group()
        self.red_ship = Ship(self, "images/ship_red.bmp", red_controls, width // 3)
        self.blue_ship = Ship(self, "images/ship_blue.bmp", blue_controls, 2 * width // 3)
        self.ships.add(self.red_ship, self.blue_ship)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        self.ufo = Ufo(self)

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = True

        #set up end game screen
        self.font = pygame.font.SysFont(None, 80)
        self.lives_font = pygame.font.SysFont(None, 36)
        self.end_message = ""
        self.screen_rect = self.screen.get_rect()

        #cooldown timer
        self.ufo_last_shot_time = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ships.update()
                self._update_bullets()
                self._update_aliens()
                self._update_ufo_bullets()
                self.ufo.update()
                self._ufo_fire_bullet()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_q:
            sys.exit()
        for ship in self.ships:
            if event.key == ship.controls["right"]:
                ship.moving_right = True
            elif event.key == ship.controls["left"]:
                ship.moving_left = True
            elif event.key == ship.controls["fire"]:
                self._fire_bullet(ship)


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        for ship in self.ships:
            if event.key == ship.controls["right"]:
                ship.moving_right = False
            elif event.key == ship.controls["left"]:
                ship.moving_left = False


    def _fire_bullet(self, ship):
        """Create a new bullet and add it to the bullets group."""

        #add the cooldown instead of having limit on the number of bullets
        current_time = pygame.time.get_ticks()

        if current_time - ship.last_shot_time >= self.settings.bullets_cooldown:
            new_bullet = Bullet(self, ship)
            self.bullets.add(new_bullet)
            ship.last_shot_time = current_time

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _ufo_fire_bullet(self):
        """Create a new ufo bullet and add it to the bullets group."""

        current_time = pygame.time.get_ticks()

        if current_time - self.ufo_last_shot_time >= self.settings.ufo_bullets_cooldown:
            new_bullet = UfoBullet(self)
            self.ufo_bullets.add(new_bullet)
            self.ufo_last_shot_time = current_time

    def _update_ufo_bullets(self):
        self.ufo_bullets.update()
        """Update the positions of the ufo bullets and get rid the of ones that reach the bottom"""

        #test 3: test if the ufo fires a bullet every while based on the cooldown indicated in the setting
        #expected result: the ufo fires a red and wide bullet (as indicated in the ufo_bullet file) that goes down the screen
        #                 and disappears once hitting the bottom of the screen\

        #test 4: test if the ufo bullet disappears once hitting the ship, then reset the game
        #expected result: the ufo bullet disappears when hitting the ship, the game should restart
        #                 the alien fleet, ship, and ufo should return to their original positions, and the number of ships left should decrease

        for bullet in self.ufo_bullets.copy():
            if bullet.rect.bottom >= self.settings.screen_height:
                self.ufo_bullets.remove(bullet)

        self._check_ufo_bullet_ship_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and print end game message.
            self.bullets.empty()
            self._create_fleet()
            self.game_active = False
            self.end_message = "YOU WIN"

    def _check_ufo_bullet_ship_collisions(self):
        """Respond to collisions between the ufo bullet and the ships"""
        collisions = pygame.sprite.groupcollide(self.ships, self.ufo_bullets, False, True)
        if collisions:
            self._ship_hit(list(collisions.keys()))


    def _reset_round(self):
        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()
        self.ufo_bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        for ship in self.ships:
            ship.center_ship()

        # Pause.
        sleep(0.5)

    def _ship_hit(self, hit_ships):
        """Respond to the ship being hit by an alien."""
        for ship in hit_ships:
            if ship.ships_left > 0:
                # Decrement ships_left.
                ship.ships_left -= 1
            else:
                ship.kill()

        if self.ships:
            self._reset_round()
        else:
            self.game_active = False
            self.end_message = "GAME OVER"

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        hit_ships = [ship for ship in self.ships
                     if pygame.sprite.spritecollideany(ship, self.aliens)]
        if hit_ships:
            self._ship_hit(hit_ships)
            return

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit(self.ships.sprites())
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, (alien_height + 25)
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _draw_lives(self):
        """Show each player's ships left in the top corners."""
        #Red player, top left.
        if self.red_ship.alive():
            red_text = f"Red: {self.red_ship.ships_left}"
        else:
            red_text = "Red: OUT"
        red_image = self.lives_font.render(red_text, True, (200, 30, 30))
        red_rect = red_image.get_rect()
        red_rect.topleft = (20, 20)
        self.screen.blit(red_image, red_rect)

        #Blue player, top right.
        if self.blue_ship.alive():
            blue_text = f"Blue: {self.blue_ship.ships_left}"
        else:
            blue_text = "Blue: OUT"
        blue_image = self.lives_font.render(blue_text, True, (30, 70, 220))
        blue_rect = blue_image.get_rect()
        blue_rect.topright = (self.screen_rect.right - 20, 20)
        self.screen.blit(blue_image, blue_rect)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for ship in self.ships:
            ship.blitme()
        self._draw_lives()
        self.ufo.blitme()
        self.aliens.draw(self.screen)

        for bullet in self.ufo_bullets.sprites():
            bullet.draw_ufo_bullet()

        #end game screen
        #test 5: test if the end game message appears on the screen when the game ends
        #expected result: if the player kills all the aliens, the screen should display YOU WIN
        #                 if the player loses all the lives, the screen should display GAME OVER
        message = self.font.render(self.end_message, True, (0,0,0))
        message_rect = message.get_rect()
        message_rect.center = self.screen_rect.center
        self.screen.blit(message, message_rect)

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
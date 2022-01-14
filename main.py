# Bounce
# Author: Noel Rebiffe
# 14 January 2022

# Bouncing survival game
# Only in control of the vertical movement of the ball, you must dodge obstacles and bounce off the sides of the screen
# as many times as you can

import pygame

pygame.init()

WHITE =(255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 800
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE  = "Bounce"


class Player(pygame.sprite.Sprite):
    """Player

    Attributes:
        image: visual representation
        rect: mathematical representation
        x_vel: horizontal velocity in px/sec
        y_vel: vertical velocity in px/sec
    """

    def __init__(self):
        """Player constructor"""

        # Call parent constructor
        super().__init__()

        # Load sprite
        self.image = pygame.Surface((18, 18))

        # get rect
        self.rect = self.image.get_rect()

        # Set velocities
        self.x_vel = 8
        self.y_vel = 0

    def update(self):
        """Changes to the player"""

        # Moving up and down
        self.rect.y += self.y_vel

    def move_up(self):
        """Called when the user presses W"""
        self.y_vel = -8

    def move_down(self):
        """Called when the user presses S"""
        self.y_vel = 8


class Blocker(pygame.sprite.Sprite):
    """The Obstacles"""


def main() -> None:
    """Driver of the Python script"""
    # Create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    # Create some local variables that describe the environment
    done = False
    clock = pygame.time.Clock()

    # ------------- MAIN LOOP
    while not done:
        # --------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # --------- CHANGE ENVIRONMENT


        # --------- DRAW THE ENVIRONMENT
        screen.fill(WHITE)

        # Update screen
        pygame.display.flip()

        # --------- CLOCK TICK
        clock.tick(75)


if __name__ == "__main__":
    main()

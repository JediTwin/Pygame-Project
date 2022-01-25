# Bounce
# Author: Noel Rebiffe
# 14 January 2022

# Bouncing survival game
# Only in control of the vertical movement of the ball, you must dodge obstacles and bounce off the sides of the screen
# as many times as you can

# draw_text appropriated from George's Jungle Jam

import pygame
import random
import time

from pygame import mixer

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 800
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE  = "Bounce"

font_name = pygame.font.Font("./data/PixeloidSans.ttf", 25)

wall_hit = pygame.mixer.Sound("./sounds/Pong_hit.mp3")

death_sound = pygame.mixer.Sound("./sounds/Galaga_death.mp3")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("./data/PixeloidSans.ttf", size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


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
        self.x_vel = -6
        self.y_vel = 0

        self.hp = 3

    def update(self):
        """Changes to the player"""

        # Moving up and down
        self.rect.y += self.y_vel

        # Moving to the side
        self.rect.x += self.x_vel

    def move_up(self):
        """Called when the user presses W"""
        self.y_vel = -8

    def move_down(self):
        """Called when the user presses S"""
        self.y_vel = 8

    def stop_move(self):
        """When the user releases a movement key"""
        self.y_vel = 0


class Block(pygame.sprite.Sprite):
    """The Obstacles"""

    def __init__(self):
        """What is block"""
        super().__init__()

        self.image = pygame.Surface((4, 50))

        self.rect = self.image.get_rect()

        # Define block location
        self.rect.x, self.rect.y = (
            random.randrange(int(SCREEN_WIDTH / 3), int(SCREEN_WIDTH / 3) * 2),
            random.randrange(SCREEN_HEIGHT)
        )


def main() -> None:
    """Driver of the Python script"""
    # Create the screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)

    # Create some local variables that describe the environment
    done = False
    clock = pygame.time.Clock()
    score = -1
    num_obstacles = 5
    game_over = True
    time_ended = 0.0
    endgame_wait = 5
    high_score = 0

    def menu_screen():
        screen.fill(WHITE)
        # Draw the menu
        draw_text(screen, "Bounce", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        draw_text(screen, "Use W and S to move!", 32, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text(screen, "Press space to start!", 32, SCREEN_WIDTH / 2, (SCREEN_HEIGHT - SCREEN_HEIGHT / 3))
        draw_text(screen, "Don't get hit more than twice!", 32, SCREEN_WIDTH / 2, (SCREEN_HEIGHT - SCREEN_HEIGHT / 4))
        pygame.display.flip()
        waiting = True
        # Check inputs
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    # Player
    player = Player()

    # Add to sprite groups
    all_sprites = pygame.sprite.Group()
    block_sprites = pygame.sprite.Group()

    # ------------- MAIN LOOP
    while not done:
        if game_over:
            # Check Score
            if score > high_score:
                high_score = score
            # Show menu
            menu_screen()
            # Reset Game
            score = -1
            player.hp = 3
            for block in block_sprites:
                block.kill()
            player.rect.x = 0
            player.rect.y = 0
            player.x_vel = -6
            time.ended = 0.0
            # Start game
            game_over = False

        # --------- EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move_up()
                if event.key == pygame.K_s:
                    player.move_down()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.stop_move()

        # --------- CHANGE ENVIRONMENT
        if not game_over:
            all_sprites.add(player)
            # Screen bounds
            if player.rect.top < 0:
                player.rect.top = 0
            if player.rect.bottom > SCREEN_HEIGHT:
                player.rect.bottom = SCREEN_HEIGHT

            # Bouncing
            if player.rect.left > SCREEN_WIDTH or player.rect.right < 0:
                player.x_vel = -player.x_vel
                score += 1

                wall_hit.play()

                # Place blocks
                for i in range(num_obstacles):
                    # Create a block
                    block = Block()
                    # Add block to sprite groups
                    all_sprites.add(block)
                    block_sprites.add(block)

            all_sprites.update()

            # Check collisions
            blocks_hit = pygame.sprite.spritecollide(player, block_sprites, True)

            for i in blocks_hit:
                player.hp -= 1
                for block in block_sprites:
                    block.kill()
                score -= 2

            if player.hp <= 0:
                all_sprites.remove(player)
                player.kill()
                player.x_vel = 0

                death_sound.play()

                game_over = True

        # --------- DRAW THE ENVIRONMENT
        screen.fill(WHITE)

        # Draw sprite
        all_sprites.draw(screen)

        # Draw Score
        draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH/10, SCREEN_HEIGHT/10)

        draw_text(screen, f"High-Score: {high_score}", 24, SCREEN_WIDTH/10, SCREEN_HEIGHT/8)

        # Update screen
        pygame.display.flip()

        # --------- CLOCK TICK
        clock.tick(75)


if __name__ == "__main__":
    main()

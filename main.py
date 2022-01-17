# Bounce
# Author: Noel Rebiffe
# 14 January 2022

# Bouncing survival game
# Only in control of the vertical movement of the ball, you must dodge obstacles and bounce off the sides of the screen
# as many times as you can

import pygame, random

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
    score = 0
    num_obstacles = 5
    game_state = "running"

    endgame_messages = {
        "lose": "Sorry, they got you. Play again!",
    }

    font = pygame.font.Font("./data/PixeloidSans.ttf", 25)

    # Player
    player = Player()

    # Add to sprite groups
    all_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    block_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    # ------------- MAIN LOOP
    while not done:
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

            if player.hp <= 0:
                game_state = "lose"

        # --------- CHANGE ENVIRONMENT

        if player.rect.left > SCREEN_WIDTH or player.rect.right < 0:
            player.x_vel = -player.x_vel
            score += 1

            # Place blocks
            for i in range(num_obstacles):
                # Create a block
                block = Block()
                # Add block to sprite groups
                all_sprites.add(block)
                block_sprites.add(block)

        # screen boundary
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > SCREEN_HEIGHT:
            player.rect.bottom = SCREEN_HEIGHT

        all_sprites.update()

        # Check collisions
        blocks_hit = pygame.sprite.spritecollide(player, block_sprites, True)

        for block in blocks_hit:
            player.hp -= 1

        # --------- DRAW THE ENVIRONMENT
        screen.fill(WHITE)

        # Draw sprite
        all_sprites.draw(screen)

        # Draw lose text
        if game_state == "lose":
            screen.blit(
                font.render(endgame_messages["lose"], True, BLACK),
                (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3)
            )

        # Update screen
        pygame.display.flip()

        # --------- CLOCK TICK
        clock.tick(75)


if __name__ == "__main__":
    main()

import pygame
import sys
import random

# Static Global Variables
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BLOCK_SIZE = 20

# Colors
DARK_GREEN = (155, 202, 82)
LIGHT_GREEN = (177, 215, 96)
SNAKE_BLUE = (70, 109, 239)
APPLE_RED = (234, 63, 38)

# Direction
UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

# Setup
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

# Sound Effects
eatSound = pygame.mixer.Sound("Omnomnom.wav")
ouch = pygame.mixer.Sound("Yeoww.wav")
hitwall = pygame.mixer.Sound("Pkhh.wav")
yeet = pygame.mixer.Sound("Yeet.wav")


class Snake(object):
    def __init__(self):
        self.length = 1
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [
            (
                ((SCREEN_WIDTH / 2) - (BLOCK_SIZE / 2)),
                ((SCREEN_HEIGHT / 2) - (BLOCK_SIZE / 2)),
            )
        ]

    def get_head_position(self):
        return self.positions[0]

    def grow(self):
        self.length += 1

    def draw(self, win):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(win, SNAKE_BLUE, r)

            # Draws a thin green border around the snake to make it more flush with environment
            pygame.draw.rect(win, LIGHT_GREEN, r, 1)

    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (
            ((cur[0] + (x * BLOCK_SIZE))),
            (cur[1] + (y * BLOCK_SIZE)),
        )

        # If snake hits itself
        if len(self.positions) > 3 and new in self.positions[2:]:
            ouch.play()
            self.reset()
        elif (
            new[0] < 0
            or new[0] > SCREEN_WIDTH - BLOCK_SIZE
            or new[1] < 0
            or new[1] > SCREEN_HEIGHT - BLOCK_SIZE
        ):
            hitwall.play()
            self.reset()

        # Reflects new position change
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def turn(self, point):
        if self.length > 1 and ((point[0] * -1), (point[1] * -1)) == self.direction:
            return
        else:
            yeet.play()
            self.direction = point

    def reset(self):
        # Add feature to wait for user response
        self.length = 1
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [
            (
                ((SCREEN_WIDTH / 2) - (BLOCK_SIZE / 2)),
                ((SCREEN_HEIGHT / 2) - (BLOCK_SIZE / 2)),
            )
        ]

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


def drawGrid(win):
    for y in range(0, int(SCREEN_HEIGHT)):
        for x in range(0, int(SCREEN_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect(
                    (x * BLOCK_SIZE, y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(win, DARK_GREEN, r)
            else:
                rr = pygame.Rect(
                    (x * BLOCK_SIZE, y * BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE)
                )
                pygame.draw.rect(win, LIGHT_GREEN, rr)


class Apple(object):
    def __init__(self):
        self.position = (0, 0)
        self.newPos()

    def newPos(self):
        self.position = (
            (random.randint(0, (SCREEN_WIDTH / BLOCK_SIZE) - 1) * BLOCK_SIZE),
            (random.randint(0, (SCREEN_HEIGHT / BLOCK_SIZE) - 1) * BLOCK_SIZE),
        )

    def draw(self, win):
        r = pygame.Rect((self.position[0], self.position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(win, APPLE_RED, r)

        # Thin border to blend with grass better
        pygame.draw.rect(win, LIGHT_GREEN, r, 1)


def main():
    # Objects
    snake = Snake()
    apple = Apple()
    score = 0

    while True:
        # Refresh
        clock.tick()
        drawGrid(win)
        snake.handle_keys()

        snake.draw(win)
        apple.draw(win)
        snake.move()

        # Check for eating collisions
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.newPos()
            eatSound.play()
            score += 1

        # Check for death
        if snake.length == 1:
            score = 0

        # Update Score
        text = "Snake - Score: {0}".format(score)
        pygame.display.set_caption(text)

        pygame.display.update()


main()

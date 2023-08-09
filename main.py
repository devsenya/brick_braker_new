import math
from typing import Tuple

import pygame

import os

from level_1 import levels
from brick_types import brick_type


class Paddle(pygame.sprite.Sprite):
    VEL = 10

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/paddle.png')
        self.rect = self.image.get_rect()

        self.width = self.rect[2]
        self.height = self.rect[3]
        self.rect.center = (WIDTH // 2, HEIGHT - self.height)

    def draw(self, win):
        paddle_sprite.update()
        paddle_sprite.draw(win)

    def move(self, direction=1):
        self.rect.x = self.rect.x + self.VEL * direction


class Ball:

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_vel = 0
        self.VEL = 5
        self.y_vel = -1

    def move(self):
        self.x += self.x_vel * self.VEL
        self.y += self.y_vel * self.VEL

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def set_positions(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def ball_floor_collision(balls, paddle):
    global lives
    for ball in balls:
        if ball.y + ball.radius >= HEIGHT:
            balls.remove(ball)
            if len(balls) <= 0:
                lives -= 1
                # центровка площади после потери жизни
                # paddle.rect.centerx = WIDTH // 2

                bonus_plus_ball(ball := Ball(paddle.rect.centerx, paddle.rect.y - ball.radius, BALL_RADIUS, "white"),
                                mass_balls)
                ball.VEL = 0
                ball.set_vel(0, ball.VEL * -1)


def bonus_plus_ball(ball, mass):
    mass.append(ball)


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, typeB: dict):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.name = typeB["type"]
        for i in typeB["images"]:
            self.images.append(pygame.image.load(i))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        # # уменьшим размер кирпичика
        # self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2))

        self.width = self.rect[2]
        self.height = self.rect[3]
        self.health = typeB["health"]
        self.max_health = self.health

        self.rect.center = (x + self.width // 2, y + self.height // 2)

    def draw(self, win):
        # pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        all_sprites.update()
        all_sprites.draw(win)

    def collide(self, ball):
        if (self.rect.y < ball.y - ball.radius <= self.rect.y + self.height) and (
                self.rect.x - ball.radius < ball.x < self.rect.x + self.width + ball.radius):
            # print(" удар снизу")
            self.hit()
            ball.set_positions(ball.x, ball.y + ball.VEL)
            ball.set_vel(ball.x_vel, ball.y_vel * -1)
            return True
        # удар справа
        if (ball.x + ball.radius >= self.rect.x) and (ball.x + ball.radius < self.rect.x + self.width) and (
                self.rect.y < ball.y < self.rect.y + self.height):
            # print(" удар справа")
            self.hit()
            ball.set_vel(ball.x_vel * -1, ball.y_vel)
            return True
        if (ball.x - ball.radius <= self.rect.x + self.width) and (ball.x - ball.radius > self.rect.x) and (
                self.rect.y < ball.y < self.rect.y + self.height):
            # print(" удар слева")
            self.hit()
            ball.set_vel(ball.x_vel * -1, ball.y_vel)
            return True
        if (self.rect.y <= ball.y + ball.radius < self.rect.y + self.height) and (
                self.rect.x - ball.radius < ball.x < self.rect.x + self.width + ball.radius):
            # print(" удар сверху")
            self.hit()
            ball.set_positions(ball.x, ball.y - ball.VEL)
            ball.set_vel(ball.x_vel, ball.y_vel * -1)
            return True

        return False

    def hit(self):
        self.health -= 1
        if self.index < len(self.images) - 1:
            self.index += 1

        self.image = self.images[self.index]


def draw(win, paddle, balls, bricks, lives, background):
    win.fill("white")
    win.blit(background, background.get_rect())
    paddle.draw(win)
    # ball.draw(win)
    for x in balls:
        x.draw(win)
    bricks.draw(win)

    lives_text = LIVES_FONT.render(f"Lives: {lives}", 1, "white")
    win.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 10))
    pygame.display.update()


def ball_collision(ball):
    # удар о левую стенку
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
    # удар о правую стенку
    if ball.y + BALL_RADIUS >= HEIGHT or ball.y - BALL_RADIUS <= 0:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)


def ball_paddle_collision(ball, paddle):
    # если шарик вне положения площадки по X, то нечего не делай
    if not (ball.x <= paddle.rect.x + paddle.width and ball.x >= paddle.rect.x):
        return

    # если шарик вне положения площадки по Y, то нечего не делай
    if not (ball.y + ball.radius >= paddle.rect.y):
        return

    distance_to_center = ball.x - paddle.rect.centerx

    percent_width = distance_to_center / paddle.width
    angle = percent_width * 90
    angle_radians = math.radians(angle)
    x_vel = math.sin(angle_radians)
    y_vel = math.cos(angle_radians) * -1
    # когда шарик касается площадки или появляется на ней, направление становится вертикальным
    # можно разбить на 2 функции(коллизия с площадкой и просчет направления)
    ball.set_vel(x_vel, y_vel)


def generate_bricks():
    brick = Brick(0, 0, brick_type(1))
    width = brick.width
    height = brick.height
    windowSize = pygame.display.get_window_size()
    bricksMap = levels(2)
    cols = len(bricksMap[0])
    rows = len(bricksMap)
    gap = (windowSize[0] - (width * cols)) // (cols + 1)

    if len(all_sprites) > 0:
        for i in all_sprites:
            all_sprites.remove(i)
    for row in range(rows):
        for col in range(cols):
            x = gap + col * (width + gap)
            y = 5 + row * (height + 5)
            if bricksMap[row][col]:
                brick = Brick(x, y, brick_type(bricksMap[row][col]))
                all_sprites.add(brick)

            print(x, y)
    print(all_sprites)
    # return all_sprites


# настройка папки ассетов

game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'img')

background_img = pygame.image.load(os.path.join(img_folder, 'back2.png'))

pygame.init()

WIDTH, HEIGHT = 1200, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("brick breaker")

FPS = 60
BALL_RADIUS = 10

LIVES_FONT = pygame.font.SysFont("comicsans", 40)

all_sprites = pygame.sprite.Group()
paddle_sprite = pygame.sprite.Group()

mass_balls = []
lives = 3


def main():
    global lives
    clock = pygame.time.Clock()

    paddle = Paddle()

    mass_balls.append(Ball(WIDTH / 2, paddle.rect.y - BALL_RADIUS, BALL_RADIUS, "white"))
    generate_bricks()
    paddle_sprite.add(paddle)

    def reset():
        global mass_balls
        mass_balls = mass_balls[:1]
        mass_balls[0].set_positions(paddle.rect.centerx, paddle.rect.y - mass_balls[0].radius)
        mass_balls[0].VEL = 0

    def display_text(text):
        text_render = LIVES_FONT.render(text, 1, "red")
        win.blit(text_render, (WIDTH / 2 - text_render.get_width() / 2, HEIGHT / 2 - text_render.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(3000)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for x in mass_balls:
                x.VEL = 10
                print(x.x_vel, x.y_vel)

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP]:

            if keys[pygame.K_LEFT] and paddle.rect.x - paddle.VEL >= 0:
                paddle.move(-1)
            if keys[pygame.K_RIGHT] and paddle.rect.x + paddle.VEL + paddle.width <= WIDTH:
                paddle.move(1)
            # если скорость = 0 -> следуем за paddle
            if len(mass_balls) == 1 and mass_balls[0].VEL == 0:
                mass_balls[0].set_positions(paddle.rect.centerx, paddle.rect.y - mass_balls[0].radius)
            if keys[pygame.K_UP]:
                mass_balls[0].VEL = 5

        # ball.move()
        for x in mass_balls:
            x.move()
            ball_collision(x)
            ball_paddle_collision(x, paddle)
        # ball_collision(ball)
        # ball_paddle_collision(ball, paddle)

        for brick in all_sprites:
            for tekBall in mass_balls:
                brick.collide(tekBall)
                # тут мы знаем какой фарик ударил по кирпичику

            if brick.health <= 0:
                all_sprites.remove(brick)

                if brick.name == "bonus_pb":
                    bonus_plus_ball(Ball(paddle.rect.centerx, paddle.rect.y - BALL_RADIUS, BALL_RADIUS, "white"),
                                    mass_balls)

                # print(mass_balls)
                brick.update()

        ball_floor_collision(mass_balls, paddle)

        if lives <= 0:
            generate_bricks()
            lives = 3
            reset()
            display_text("You Lost!")

        if len(all_sprites) == 0:
            generate_bricks()
            lives = 3
            reset()
            display_text("You Won!")

        draw(win, paddle_sprite, mass_balls, all_sprites, lives, background_img)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()

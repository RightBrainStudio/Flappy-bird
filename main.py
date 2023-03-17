import pygame
import math
import random

pygame.font.init()

pygame.font.get_init()

font1 = pygame.font.SysFont('freesanbold.ttf', 50)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, img, height, width):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        screen.blit(self.image, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect
        self.mask = pygame.mask.from_surface(self.image)


bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (480, 322))
ground = pygame.image.load("ground.png")
ground = pygame.transform.scale(ground, (480, 14))
start = 0
clock_counter = 0

pygame.init()
screen = pygame.display.set_mode((480, 360))
clock = pygame.time.Clock()
running = True
dt = 0

gravity = 0

player = Sprite("R.png", 30, 30)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

pygame.display.set_caption("Flappy bird")

pipe_x = 500
pipe_y = random.randrange(-230, -70)
pipe = "pipe2.png"
pipe1_2 = Sprite(pipe, 257.5, 50)
pipe1_2.rect = (pipe_x, pipe_y)
pipe = "pipe.png"
pipe1_1 = Sprite(pipe, 257.5, 50)
pipe1_1.rect = (pipe_x, pipe_y + 360)

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(player)

all_sprites_list.add(pipe1_1)
all_sprites_list.add(pipe1_2)


def check_collision():
    global start
    if (player_pos.y < 0) or (player_pos.y > 322) or 0 or (
            (player_pos.x > pipe_x - 25) and (pipe_x + 25 > player_pos.x) and not (
            pipe_y + 250 < player_pos.y < pipe_y + 335)):
        start = 0


temp_bool = False
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # game loop

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        if start == 0:
            temp_bool = False
            start = 1
        else:
            gravity = 0
            player_pos.y -= 300 * dt
            check_collision()

    if start == 1:
        gravity += 200 * dt
        player_pos.y += gravity * dt
    else:
        player_pos.y = screen.get_height() / 2 + (math.sin(math.radians(clock_counter)) * 20)
        score = 0

    clock_counter += 300 * dt

    check_collision()

    player.rect = player_pos

    if start == 1 and pipe_x > -40:
        pipe_x -= 150 * dt

    else:
        pipe_x = 500
        pipe_y = random.randrange(-230, -70)

    pipe1_2.rect = (pipe_x, pipe_y)
    pipe1_1.rect = (pipe_x, pipe_y + 360)

    all_sprites_list.update()

    screen.blit(bg, (0, 0))

    all_sprites_list.draw(screen)

    pygame.draw.rect(screen, (233, 231, 211), pygame.Rect(0, 315, 480, 45))

    screen.blit(ground, (-0.5 * clock_counter % 480, 315))

    screen.blit(ground, (-0.5 * clock_counter % 480 - 480, 315))

    if not temp_bool and (pipe_x - 25 < player_pos.x < pipe_x + 25):
        score += 1
        temp_bool = True
    elif temp_bool and not (pipe_x - 25 < player_pos.x < pipe_x + 25):
        temp_bool = False

    text1 = font1.render("Score {}".format(score), True, (0, 0, 0))

    textRect1 = text1.get_rect()

    textRect1.center = (240, 20)

    screen.blit(text1, textRect1)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
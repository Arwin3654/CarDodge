import random
import time
import pygame
from pygame import mixer

pygame.init()
pygame.font.init()
pygame.mixer.init()
crash = pygame.mixer.Sound("item/explotion.wav")
# WINDOW
WIN_WIDTH = 500
WIN_HEIGHT = 800
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


# ENEMY_CARS
ENEMY_WIDTH = 70
ENEMY_HEIGHT = 140
ENEMY_VEL = 1

# PLAYER
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 140
PLAYER_VEL = 5
player = pygame.transform.scale(pygame.image.load(
    "item/car.webp"), (PLAYER_WIDTH, PLAYER_HEIGHT))

# DISPLAY_TEXT
FONT = pygame.font.SysFont("comics", 50)

pygame.display.set_caption("Car Dodge")
pygame.display.set_icon(pygame.image.load('item/car.png'))
BG = pygame.transform.scale(pygame.image.load("item/Road.png"), (500, 1000))


def draw_bg():
    WINDOW.blit(BG, (0, 0))


def draw_player(x, y):
    WINDOW.blit(player, (x, y))


def draw_enemies(enemies):
    for enemy in enemies:
        WINDOW.blit(pygame.transform.scale(pygame.image.load(
            "item/car.webp"), (ENEMY_WIDTH, ENEMY_HEIGHT)), enemy)


def enemies_move(enemies, enemy_vel):
    for enemy in enemies:
        enemy.y += enemy_vel


def main():
    # ENEMY
    enemy_count = 0
    enemies = []
    enemy_add_increment = 1
    max_enemy_add_increment = 70
    max_enemy_on_screen = 5

    hit = False

    clock = pygame.time.Clock()
    start_time = time.time()

    x = WIN_WIDTH - 300 / 2 - player.get_width() / 2
    y = 680

    running = True

    while running:

        enemy_count += 1
        clock.tick(60)
        elapsed_time = time.time() - start_time
        time_text = FONT.render(f"{(round(elapsed_time))}s", 1, "black")
        # ENEMY CREATION
        if enemy_count > enemy_add_increment / 1000 and len(enemies) < 1:

            enemy_x = random.randint(80, 350)
            if 175 < enemy_x < 215:
                enemy_x = 175
            elif 255 > enemy_x > 215:
                enemy_x = 255
            enemy = pygame.Rect(enemy_x, -ENEMY_HEIGHT,
                                ENEMY_WIDTH, ENEMY_HEIGHT)
            enemies.append(enemy)
            enemy_count = 0

        enemy_vel = ENEMY_VEL + elapsed_time * 0.1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # MOVEMENT
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            x = max(79, x - PLAYER_VEL)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            x = min(WIN_WIDTH - PLAYER_WIDTH - 80, x + PLAYER_VEL)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            y = max(y - PLAYER_VEL, 380)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            y = min(y + PLAYER_VEL, 710)
        for enemy in enemies[:]:
            enemy.y += enemy_vel
            if enemy.y > WIN_HEIGHT:
                enemies.remove(enemy)
            elif enemy.y + ENEMY_HEIGHT >= y and enemy.colliderect(
                    pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)):
                enemies.remove(enemy)
                hit = True
                break

        if hit:
            crash.play()
            lost_text = FONT.render("You Lost!", 1, "red")
            WINDOW.blit(lost_text,
                        (WIN_WIDTH / 2 - lost_text.get_width() / 2, WIN_HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)
            break
        draw_bg()
        draw_player(x, y)
        draw_enemies(enemies)
        enemies_move(enemies, ENEMY_VEL)
        WINDOW.blit(time_text, (10, 10))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

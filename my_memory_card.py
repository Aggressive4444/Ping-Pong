from pygame import *
import random
from PIL import Image
from time import time as timer

# Подключение
mixer.init()
font.init()

# Константы
WIDTH = 700
HEIGHT = 500
FPS = 60

# Картинки и звуки
img_background = "background.jpg"
img_player1 = "player1.png"
img_player2 = "player2.png"
img_ball = "ball.png"

# Создание окна игры
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Пинг-Понг")
background = transform.scale(image.load(img_background), (WIDTH, HEIGHT))
clock = time.Clock()

# Шрифты
font1 = font.SysFont('Arial', 36)

# Загрузка изображений
player1_img = transform.scale(image.load(img_player1), (70, 100))  
player1_img = transform.flip(player1_img, True, False)  
player2_img = transform.scale(image.load(img_player2), (70, 100))  
ball_img = transform.scale(image.load(img_ball), (30, 30))

# Классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = player_image
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

class Racket(GameSprite):
    def move(self, up_key, down_key):
        keys = key.get_pressed()
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.speed_x = player_speed
        self.speed_y = player_speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

        if self.rect.left <= 0:
            global score_right
            score_right += 1
            self.reset_position()

        if self.rect.right >= WIDTH:
            global score_left
            score_left += 1
            self.reset_position()

    def reset_position(self):
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.speed_x *= -1

# Создание объектов
player1 = Racket(player1_img, 30, HEIGHT // 2 - 50, 5, 70, 100)  
player2 = Racket(player2_img, WIDTH - 100, HEIGHT // 2 - 50, 5, 70, 100)  
ball = Ball(ball_img, WIDTH // 2 - 10, HEIGHT // 2 - 10, 3, 30, 30)

all_sprites = sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

# Счетчики
score_left = 0
score_right = 0

# Основной цикл игры
running = True
finish = False
while running:
    for k in event.get():
        if k.type == QUIT:
            running = False

    if not finish:
        all_sprites.update()
        player1.move(K_w, K_s)
        player2.move(K_UP, K_DOWN)

        if sprite.collide_rect(ball, player1) or sprite.collide_rect(ball, player2):
            ball.speed_x *= -1

        window.blit(background, (0, 0))
        all_sprites.draw(window)

        # Отображение счетчиков
        text_left = font1.render("Очки левого: " + str(score_left), 1, (0, 0, 0))
        text_right = font1.render("Очки правого: " + str(score_right), 1, (0, 0, 0))
        window.blit(text_left, (10, 10))
        window.blit(text_right, (WIDTH - 270, 10))

    display.update()
    clock.tick(FPS)
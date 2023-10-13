import pygame
from pygame.locals import *
from random import randint, choice

pygame.init()

# Window settings
window_width = 700
window_height = 500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Color Switch')

# Font settings
font1 = pygame.font.SysFont('Verdana', 36)
font2 = pygame.font.SysFont('Verdana', 100)

# Game variables
clock = pygame.time.Clock()
FPS = 60
max_time = 180
score = 0

if pygame.mixer.get_init():
  pygame.mixer.music.load('colorswitchmusic.mp3')
  pygame.mixer.music.play(-1)

# Colors
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Load images
background = pygame.transform.scale(pygame.image.load('background.png'), (window_width, window_height))
player_images = {
    "red": pygame.image.load('redball.png'),
    "cyan": pygame.image.load('cyanball.png'),
    "green": pygame.image.load('greenball.png'),
    "yellow": pygame.image.load('yellowball.png')
}
obstacle_images = {
    "red": pygame.image.load('redwall.png'),
    "cyan": pygame.image.load('cyanwall.png'),
    "green": pygame.image.load('greenwall.png'),
    "yellow": pygame.image.load('yellowwall.png')
}

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Player(GameSprite):
    def __init__(self, color, x, y, speed):
        image = pygame.transform.scale(player_images[color], (40, 40))
        super().__init__(image, x, y, speed)
        self.color = color

    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        elif key_state[K_DOWN] and self.rect.bottom < window_height:
            self.rect.y += self.speed

class Obstacle(GameSprite):
    def __init__(self, color, x, y, speed):
        image = pygame.transform.scale(obstacle_images[color], (20, 165))
        super().__init__(image, x, y, speed)
        self.color = color

def show_score(score):
    score_text = font1.render('Score: ' + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

# Create player and obstacles
player = Player("red", 70, window_height // 2, 4)
obstacles = pygame.sprite.Group()

# Game loop
running = True
game_over = False
start_time = pygame.time.get_ticks()
color_change_time = pygame.time.get_ticks()
speed_increase_time = pygame.time.get_ticks()
speed_increase_interval = 60000  # Increase speed every minute
speed_increase_amount = 1  # Increase speed by 1 pixel

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if not game_over:
        # Check for collisions with obstacles
        for obstacle in obstacles:
            if pygame.sprite.collide_rect(player, obstacle):
                if player.color == obstacle.color:
                    score += 1
                else:
                    game_over = True
                    break

        # Update player and obstacles
        player.update()
        obstacles.update()

        # Spawn new obstacles
        current_time = pygame.time.get_ticks()
        if current_time - start_time > randint(1000, 2000):
            color = choice(["red", "cyan", "green", "yellow"])
            y = randint(100, window_height - 100)
            obstacle = Obstacle(color, window_width, y, 4)
            obstacles.add(obstacle)
            start_time = current_time

        # Change ball color every 10 seconds
        if current_time - color_change_time > 10000:
            player.color = choice(["red", "cyan", "green", "yellow"])
            player.image = pygame.transform.scale(player_images[player.color], (40, 40))
            color_change_time = current_time

        # Increase wall speed every minute
        if current_time - speed_increase_time > speed_increase_interval:
            for obstacle in obstacles:
                obstacle.speed += speed_increase_amount
            speed_increase_time = current_time

        # Draw background, player, obstacles, and score
        window.blit(background, (0, 0))
        window.blit(player.image, player.rect)
        obstacles.draw(window)
        show_score(score)

        # Check game over condition
        if pygame.time.get_ticks() - start_time > max_time * 1000:
            game_over = True

        # Display appropriate text when game is over
        if game_over:
            if pygame.time.get_ticks() - start_time <= max_time * 1000:
                text = font2.render("YOU LOST!", True, (255, 0, 0))
            else:
                text = font2.render("YOU WON!", True, (0, 255, 0))
            text_rect = text.get_rect(center=(window_width / 2, window_height / 2))
            window.blit(text, text_rect)

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
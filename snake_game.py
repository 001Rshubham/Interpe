# File: snake_game_with_super_food_sound.py
# Description: Snake game with background music, high score saving, power-ups, and special food sound

import pygame
import sys
import random
import time
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game Constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 7  # Slower snake

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (220, 20, 60)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)

# Fonts
font = pygame.font.SysFont("consolas", 24)
big_font = pygame.font.SysFont("consolas", 48)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("🐍 Nokia Snake Game")

clock = pygame.time.Clock()

# Load music
try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)
except:
    print("Background music not found.")

# Sound effects
eat_sound = pygame.mixer.Sound("food_G1U6tlb.mp3")
game_over_sound = pygame.mixer.Sound("sound_ErK79lZ.mp3")
super_eat_sound = pygame.mixer.Sound("super_food.mp3")  # special food sound

# Directions
DIRECTIONS = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
}

# Game Modes
MODES = ["Classic", "Time Attack", "Hard", "Infinite"]

# High score file
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    with open(HIGH_SCORE_FILE, "r") as f:
        return int(f.read().strip())

def save_high_score(score):
    high = load_high_score()
    if score > high:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, pygame.Rect(food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, BLUE, pygame.Rect(obs[0]*CELL_SIZE, obs[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_powerup(powerup, kind):
    color = CYAN if kind == "slow" else ORANGE if kind == "shrink" else PURPLE
    pygame.draw.rect(screen, color, pygame.Rect(powerup[0]*CELL_SIZE, powerup[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def get_random_position(snake, obstacles):
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake and pos not in obstacles:
            return pos

def show_message(text, subtext=""):
    screen.fill(BLACK)
    title = big_font.render(text, True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
    if subtext:
        subtitle = font.render(subtext, True, WHITE)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def game_over_screen(score):
    save_high_score(score)
    high = load_high_score()
    show_message("Game Over", f"Score: {score} | High Score: {high} | Enter=Again | Esc=Quit")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def mode_select_screen():
    selected = 0
    while True:
        screen.fill(BLACK)
        title = big_font.render("Select Game Mode", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        for i, mode in enumerate(MODES):
            color = WHITE if i != selected else GREEN
            text = font.render(mode, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + i*40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    selected = (selected - 1) % len(MODES)
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected = (selected + 1) % len(MODES)
                elif event.key == pygame.K_RETURN:
                    return MODES[selected]

def snake_game(mode):
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (1, 0)
    food = get_random_position(snake, [])
    score = 0
    speed = float(FPS)
    timer_limit = 60
    start_time = time.time()

    obstacles = []
    if mode == "Hard":
        for _ in range(10):
            obstacles.append(get_random_position(snake, []))

    powerup = None
    powerup_kind = None
    powerup_timer = 0
    double_score = False

    while True:
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        draw_obstacles(obstacles)
        if powerup:
            draw_powerup(powerup, powerup_kind)

        # UI
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if mode == "Time Attack":
            time_left = max(0, int(timer_limit - (time.time() - start_time)))
            time_text = font.render(f"Time: {time_left}", True, YELLOW)
            screen.blit(time_text, (WIDTH - 150, 10))
            if time_left <= 0:
                return score

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN and event.key in DIRECTIONS:
                new_dir = DIRECTIONS[event.key]
                if (new_dir[0]*-1, new_dir[1]*-1) != direction:
                    direction = new_dir

        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        if mode == "Infinite":
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        else:
            if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
                game_over_sound.play()
                return score

        if new_head in snake or new_head in obstacles:
            game_over_sound.play()
            return score

        snake.insert(0, new_head)

        # Check food
        if new_head == food:
            eat_sound.play()
            score += 2 if double_score else 1
            food = get_random_position(snake, obstacles)
            if mode == "Classic" and score % 5 == 0:
                speed += 0.5
            if not powerup and random.random() < 0.3:
                powerup = get_random_position(snake, obstacles)
                powerup_kind = random.choice(["slow", "shrink", "double"])
        else:
            snake.pop()

        # Check powerup
        if powerup and new_head == powerup:
            if powerup_kind == "slow":
                speed = max(FPS - 2, 3)
                super_eat_sound.play()
            elif powerup_kind == "shrink" and len(snake) > 4:
                snake = snake[:-3]
                super_eat_sound.play()
            elif powerup_kind == "double":
                double_score = True
                super_eat_sound.play()  # Play sound for super food
            powerup = None
            powerup_timer = time.time()

        if double_score and time.time() - powerup_timer > 10:
            double_score = False

        clock.tick(speed if mode != "Hard" else FPS + 5)

# Main loop
while True:
    mode = mode_select_screen()
    score = snake_game(mode)
    game_over_screen(score)

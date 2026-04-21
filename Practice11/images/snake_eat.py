import pygame
import random
import time
import os

pygame.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
ORANGE = (255, 165, 0) 

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20 

dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game: Dynamic Food Weights')

clock = pygame.time.Clock()
score_font = pygame.font.SysFont("Verdana", 25)


eat_sound = None
try:
    pygame.mixer.music.load("images/snake.wav")
    pygame.mixer.music.set_volume(0.5)
    eat_sound = pygame.mixer.Sound("images/eat_sound.wav")
except Exception as e:
    print("Sound error:", e)

def display_ui(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    dis.blit(value, [10, 10])

def generate_new_food(snake_list):
    """
    Generates food with a random weight and a timestamp.
    Returns a dictionary containing position, weight, and spawn time.
    """
    while True:
        fx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
        fy = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
        
        if [fx, fy] not in snake_list:
            
            weight = random.choice([1, 3])
        
            spawn_time = pygame.time.get_ticks() 
            return {"pos": [fx, fy], "weight": weight, "time": spawn_time}

def gameLoop():
    game_over = False
    game_close = False

    try:
        pygame.mixer.music.play(-1)
    except:
        pass

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1
    score = 0
    level = 1
    current_speed = 10 
    
   
    FOOD_LIFESPAN = 5000 
   
    food = generate_new_food(snake_list)

    while not game_over:

        while game_close:
            dis.fill(BLUE)
            msg = score_font.render("Game Over! C-Play / Q-Quit", True, RED)
            dis.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_ui(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change, x1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change, x1_change = BLOCK_SIZE, 0

        
        current_time = pygame.time.get_ticks()
        if current_time - food["time"] > FOOD_LIFESPAN:
            food = generate_new_food(snake_list) 

        # Boundary Check
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)

        food_color = GREEN if food["weight"] == 1 else ORANGE
        pygame.draw.rect(dis, food_color, [food["pos"][0], food["pos"][1], BLOCK_SIZE, BLOCK_SIZE])

        
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for block in snake_list:
            pygame.draw.rect(dis, WHITE, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

        display_ui(score, level)
        pygame.display.update()

       
        if x1 == food["pos"][0] and y1 == food["pos"][1]:
            if eat_sound:
                eat_sound.play()
            
            
            length_of_snake += food["weight"]
            score += food["weight"]
            
            new_level = (score // 5) + 1
            if new_level > level:
                level = new_level
                current_speed += 2
            
            food = generate_new_food(snake_list)

        clock.tick(current_speed)

    pygame.quit()
    quit()

gameLoop()
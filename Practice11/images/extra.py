import pygame, sys
from pygame.locals import *
import random, time


pygame.init()


FPS = 60
FramePerSec = pygame.time.Clock()


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5        
SCORE = 0      
COIN_SCORE = 0   
N = 10           


font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)


background = pygame.image.load("images/AnimatedStreet.png")

try:
    pygame.mixer.music.load("images/background.wav") 
    pygame.mixer.music.play(-1)              
except:
    print("Background music file not found")

DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/coin.png") 
        self.rect = self.image.get_rect()
        self.weight = 1 # Default weight
        self.reset()

    def move(self):
        self.rect.move_ip(0, SPEED)
      
        if (self.rect.top > 600):
            self.reset()

    def reset(self):
       
        self.weight = random.randint(1, 3)
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
                          

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

   
    DISPLAYSURF.blit(background, (0,0))
    
   
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_count = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_count, (SCREEN_WIDTH - 100, 10))

   
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

   
    collided_coin = pygame.sprite.spritecollideany(P1, coins)
    if collided_coin:
        COIN_SCORE += collided_coin.weight
        
        if COIN_SCORE // N > (COIN_SCORE - collided_coin.weight) // N:
            SPEED += 0.5
            
        collided_coin.reset() 

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()
        try:
            pygame.mixer.Sound('images/crash.wav').play()
        except:
            pass 
            
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        pygame.display.update()
        
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()         
          
    pygame.display.update()
    FramePerSec.tick(FPS)
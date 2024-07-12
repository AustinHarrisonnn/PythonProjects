import pygame
import sys
import random

pygame.init()

BLOCK_SIZE = 50
SW, SH = 800, 800
FONT = pygame.font.Font(None, BLOCK_SIZE * 2)

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Snake!")
clock = pygame.time.Clock()

background_image = pygame.image.load('C:/Users/ausgood/Desktop/PythonProjects/assets/6104132.png').convert_alpha()
FONT = pygame.font.Font(None, BLOCK_SIZE * 2)

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        global apple
        
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
        
        if self.dead:
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.xdir = 1
            self.ydir = 0
            self.dead = False
            apple = Apple()
        
        self.body.append(self.head.copy())
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.pop(0)

class Apple:
    def __init__(self):
        self.x = random.randint(0, SW // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.y = random.randint(0, SH // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.image = pygame.image.load('C:/Users/ausgood/Desktop/PythonProjects/assets/apple_15012111.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def update(self):
        screen.blit(self.image, self.rect)

def draw_grid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

snake = Snake()
apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()
    
    screen.blit(background_image, (0,0))
    draw_grid()
    apple.update()

    score = FONT.render(f"{len(snake.body) + 1}", True, "white")
    score_rect = score.get_rect(center=(SW / 2, SH / 20))
    screen.blit(score, score_rect)

    pygame.draw.rect(screen, "green", snake.head)
    for square in snake.body:
        pygame.draw.rect(screen, "green", square)

    if snake.head.colliderect(apple.rect):
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()

    pygame.display.update()
    clock.tick(10)
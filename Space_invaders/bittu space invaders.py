import math
import random
import sys
import pygame
from pygame import mixer

pygame.init()

window = pygame.display.set_mode((800,600))

pygame.display.set_caption("Space Invaders,,,")
ufo = pygame.image.load("ufo.png")
pygame.display.set_icon(ufo)

background=pygame.image.load("background.png")


playerImg = pygame.image.load("player.png")
playerx = 370
playery = 480
playerx_change = 0

bulletImg = pygame.image.load("bullet.png")
bulletx = 370
bullety = 480
bullety_change = -10
bulletx_change = 0
bullet_state = "loading"


enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
total_enemies = 6

for x in range(total_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0,736))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(4)
    enemyy_change.append(40)
        

point = 0
point_font = pygame.font.Font("freesansbold.ttf",32)
pointx = pointy = 10

game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def score_display(x,y):
    point_scored = point_font.render("Score : " + str(point), True, (255, 255, 255))
    window.blit(point_scored, (x, y))
    

def player(x,y):
    window.blit(playerImg, (x,y))

def enemy(i,x,y):
    window.blit(enemyImg[i], (x,y))

def game_over_txt():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    window.blit(over_text, (200, 250))

def bullet(x, y):
    global bullet_state
    bullet_state = "shoot"
    window.blit(bulletImg, (x + 16, y + 10))

def collide(bulletx, bullety, enemyx, enemyy):
    dis = math.sqrt(math.pow(enemyx-bulletx, 2))+(math.pow(enemyy-bullety,2)) 
    if dis < 27:
        return True
    else:
        return False
        
    
#-------------------------------------------
run = True
while run:
    
    window.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change=-5

            if event.key == pygame.K_RIGHT:
                playerx_change=5

            if event.key == pygame.K_SPACE:
                if bullet_state is "loading":
                   bulletx = playerx
                   bullet(bulletx, bullety)
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change=0
    
    playerx+=playerx_change
    if playerx <= 0:
        playerx = 0
    if playerx >= 736:
        playerx = 736
    
    if bullety<=0:
        bullety = 480
        bullet_state = "loading"

    if bullet_state is "shoot":
        bullet(bulletx, bullety)
        bullety+=bullety_change

    
    for i in range(total_enemies):
        if enemyy[i] > 440:
            for k in range(total_enemies):
                enemyy[k] = 2000
            game_over_txt()
            break
        
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 4
            enemyy[i]+= enemyy_change[i]
        elif enemyx[i]>=736:
            enemyx_change[i] = -4
            enemyy[i]+= enemyy_change[i]

        
        collision = collide(bulletx, bullety, enemyx[i], enemyy[i])
        if collision:
            bullety = 480
            bullet_state = "loading"
            point += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)

        enemy(i, enemyx[i], enemyy[i])
            
        
        
    player(playerx,playery)
    score_display(pointx,pointy)
    
    pygame.display.update()

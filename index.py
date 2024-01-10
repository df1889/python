import pygame
from pygame.rect import *
import random

def restart():
    global score, isGameOver
    for i in range(len(star)):
        rectStar[i].y = -1
    score = 0
    isGameOver = False

def eventProcess(move):
    global isActive
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                isActive = False
            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = 1
            if event.key == pygame.K_UP:
                move.y = -1
            if event.key == pygame.K_DOWN:
                move.y = 1
            if event.key == pygame.K_r:
                restart()

def movePlayer(player, current, move, isGameOver):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    if not isGameOver:
        current.x += move.x
        current.y += move.y

    if current.y > SCREEN_HEIGHT - current.height:
        current.y = SCREEN_HEIGHT - current.height
    if current.x > SCREEN_WIDTH-current.width:
        current.x = SCREEN_WIDTH - current.width
    if current.y < 0:
        current.y = 0
    if current.x < 0:
        current.x = 0
    SCREEN.blit(player, current)

def timeUpdate50ms():
    global time500ms
    time500ms += 1
    if time500ms > 5:
        time500ms = 0
        return True
    return False

def makeStar(rec):
    if timeUpdate50ms():
        idex = random.randint(0, len(star)-1)
        if rec[idex].y == -1:
            rec[idex].x = random.randint(0, SCREEN_WIDTH)
            rec[idex].y = 0

def moveStar(star, current, isGameOver):
    global SCREEN_HEIGHT
    for i in range(len(star)):    
        if current[i].y == -1:
            continue
        if not isGameOver:
            current[i].y += 1
        if current[i].y > SCREEN_HEIGHT:
            current[i].y = -1
        SCREEN.blit(star[i], current[i])

def CheckCollision(player, star):
    global isGameOver, score
    if isGameOver:
        return
    for rec in star:
        if rec.top < player.bottom \
                and player.top < rec.bottom \
                and rec.left < (player.right-8) \
                and (player.left+8) < rec.right:
            isGameOver = True
            break
    score += 1

def timeUpdate4sec(isGameOver):
    global time4Sec, time4SecToggle
    if not isGameOver:
        return False
    time4Sec += 1
    if time4Sec > 40:
        time4Sec = 0
        time4SecToggle = (~time4SecToggle)
    return time4SecToggle

def setText(isupdate=False):
    global score
    myFont = pygame.font.SysFont("arial", 20, True, False)

    SCREEN.blit(myFont.render(
        f'score : {score}', True, 'green'), (10, 10, 0, 0))

    if isupdate:
        SCREEN.blit(myFont.render(
            f'fail.', True, 'red'), (185, 290, 0, 0))


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
score = 0
isActive = True
isGameOver = False
move = Rect(0, 0, 0, 0)
time500ms = 0
time4Sec = 0
time4SecToggle = False

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("?")

player = pygame.image.load("star.png")
player = pygame.transform.scale(player, (20, 20))
rectPlayer = player.get_rect()
rectPlayer.centerx = (SCREEN_WIDTH / 2)
rectPlayer.centery = (SCREEN_HEIGHT / 2)

star = [pygame.image.load("img.jpg") for i in range(20)]
rectStar = [None for i in range(len(star))]
for i in range(len(star)):
    star[i] = pygame.transform.scale(star[i], (20, 20))
    rectStar[i] = star[i].get_rect()
    rectStar[i].y = -1

clock = pygame.time.Clock()

while isActive:
    SCREEN.fill((0, 0, 0))
    eventProcess(move)    
    movePlayer(player, rectPlayer,move,isGameOver)  
    makeStar(rectStar)
    moveStar(star, rectStar,isGameOver)
    CheckCollision(rectPlayer, rectStar)
    setText(timeUpdate4sec(isGameOver))       
    pygame.display.flip()
    clock.tick(100)
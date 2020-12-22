import pygame
import random
import math
from pygame import mixer

# initialize py game
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# 800 and 600  are respctive window width and hieght respectively x and y axis
# Background
background_img = pygame.image.load('background.png')
# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)
# -1 means it plays in the loop

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('v.png')
pygame.display.set_icon(icon)
#  Player
player_img = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0
#  Enemy
n = 6
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(n) :
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
#  Bullet
# ready-----> you can't see the bullet on the screen
# free-----> the bullet is currently moving
# bullet is going o be shot from the player y axis position
# we set it to zero because bullet moves in x direction so we have to change it while loop
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'
score = 0
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
#  we can download any font by internet and extract in the directory
textX = 10
textY = 10
# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y) :
    score = font.render('Score:' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text() :
    over_text = over_font.render('GAME OVER', True, (255, 0, 255))
    screen.blit(over_text, (200, 250))


#  function to draw playerImg in screen
def player(x, y) :
    screen.blit(player_img, (x, y))


#     blit fxn use to draw the image on the screen
# function to draw enemyImg in screen
def enemy(x, y, i) :
    screen.blit(enemy_img[i], (x, y))


def bullet_fired(x, y) :
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


# collision
def iscollision(enemyx, enemyy, bulletx, bullety) :
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27 :
        # 27 is get by trial and test method for ideal collision
        return True
    else :
        return False


#     x+16 and y+10 beacuse we have to have the bullet at the top of the player


# to avoid an infinite loop we assign a varible with value true
#  game loop
running = True
while running :
    # R,G,B----->RED,GREEN,BLUE THE VALUE OF INDIVIUAL CAN GO UPTO 255
    # screen.fill((128, 0, 128))
    # background image
    screen.blit(background_img, (0, 0))
    #  beacuse image is of 800*600
    # now when we read this 226 kb big png file the whilw loop iteration become slow so we have to change values to approx 5

    for event in pygame.event.get() :
        # when we press the cross button the infinte loop will stop so for that
        if event.type == pygame.QUIT :
            running = False
        #   if key stroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                playerX_change = -7
            if event.key == pygame.K_RIGHT :
                playerX_change = 7
            if event.key == pygame.K_SPACE :
                if bullet_state == 'ready' :
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    # get the current x coordinte of the spaceship
                    bullet_fired(bulletX, bulletY)
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0
    playerX = playerX + playerX_change
    if playerX <= 0 :
        playerX = 0
    elif playerX >= 736 :
        playerX = 736
    #     we have to consider size also we know that size of player is 64 so 800-64=736
    # enemy movement
    for i in range(n) :
        # game over
        if enemyY[i] > 420 :
            for j in range(n) :
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] = enemyX[i] + enemyX_change[i]

        if enemyX[i] <= 0 :
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736 :
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        collison = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison :
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_state = 'ready'
            bulletY = 480
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 150)
        enemy(enemyX[i], enemyY[i], i)

    #     bullet movement
    if bulletY <= 0 :
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire' :
        bullet_fired(bulletX, bulletY)
        bulletY -= bulletY_change
    #     collision

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

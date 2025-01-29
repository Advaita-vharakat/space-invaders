import pygame
import math
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background music.mp3')
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("SPACE HERO")
icon = pygame.image.load('shuttle.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 510
playerX_change = 0

# Enemy
enemy1img = []
enemy1X = []
enemy1Y = []
enemy1X_change = []
enemy1Y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy1img.append(pygame.image.load('enemy1.png'))
    enemy1X.append(random.randint(0, 730))
    enemy1Y.append(random.randint(50, 150))
    enemy1X_change.append(0.4)
    enemy1Y_change.append(40)

# bullet
# "ready"---> you cant see the bullet on the screen
# "fire"----> the bullet is currently moving

bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2.5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 35)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 66)
restart_font = pygame.font.Font('freesansbold.ttf', 20)

game_over = False

def game_over_():
    global game_over
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    restart_text = restart_font.render(".", True, (255, 255, 255))
    screen.blit(restart_text, (280, 350))
    game_over = True


def show_score(x , y):
    score = font.render("Score : " + str(score_value),True, (255 , 255, 255))
    screen.blit(score,(x,y))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy1(x, y, i):
    screen.blit(enemy1img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))

def iscollusion(bulletY,bulletX,enemy1X,enemy1Y):
    distance= math.sqrt(math.pow(enemy1X-bulletX, 2)+(math.pow(enemy1Y-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

#game loop
running = True
while running:
    screen.fill((23, 45, 67))
    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed check whether it is right or left
        # making our player move according to the command given
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('bullet shoot.mp3')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_q and game_over == True:
                score_value = 0
                game_over = False




    # creating boundries to the space ship
    if playerX <= 0:
        playerX = 0
    if playerX >= 730:
        playerX = 730

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemy1Y[i] > 440:
            for j in range(num_of_enemies):
                enemy1Y[j] = 2000
            game_over_()
            bulletX_change = 0
            bulletY_change = 0
            playerX = 370
            playerY = 510
            playerX_change = 0

        enemy1X[i] += enemy1X_change[i]
        if enemy1X[i] <= 0:
            enemy1X_change[i] = 0.4
            enemy1Y[i] += enemy1Y_change[i]
        if enemy1X[i] >= 730:
            enemy1X_change[i] = -0.4
            enemy1Y[i] += enemy1Y_change[i]


        # collusion
        collusion = iscollusion(bulletY, bulletX, enemy1X[i], enemy1Y[i])
        if collusion:
            bulletX = 0
            bulletY = 480
            bullet_state = "ready"
            explosion_sound = mixer.Sound('explosion.mp3')
            explosion_sound.play()
            score_value += 1
            enemy1X[i] = random.randint(0, 730)
            enemy1Y[i] = random.randint(50, 150)

        enemy1(enemy1X[i], enemy1Y[i], i)

    #Bullet movement
    if bulletY<0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -=bulletY_change


    playerX += playerX_change
    iscollusion(bulletY, bulletX, enemy1X[i], enemy1Y[i])
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
    
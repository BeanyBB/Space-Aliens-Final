"""
Pogram: Space invaders
Author: Ben B
First Made:12/8/19
Last edited: 12/20/19

Degree of difficulty:
1. [x] Add graphics to enemy, ship, and bullet. (+2pts)
2. [x] Make multiple levels. (+2pts)
3. [] Add sound effects. (+1pts)
4. [x] Make background interesting. (+1pts)
5. [x] Add a score to the program. (+2pts)
""" 

import pygame
import time
import random
import math


#
# Initializing pygame
#
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Aliens')
clock = pygame.time.Clock()

#
# creating colors
#
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0) 
blue = (0, 0, 128) 

#
# Getting and loading images
#
shipImg = pygame.image.load('spaceShip.png')
bulletImg = pygame.image.load('bullet.png')
background = pygame.image.load('spaceBack.jpg')
enemy = pygame.image.load('enemy.png')
explosionImg = pygame.image.load('explosion.png')

#
# Score print stuff
#
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10



def explosion(x,y):
    """ Prints explosion image on the screen"""
    screen.blit(explosionImg, (x,y))

def fire_bullet(x,y):
    """ Makes it so the bullet will be able to move and displays"""
    global bullet_state
    bullet_state = True
    #
    # Prints bullet
    #
    screen.blit(bulletImg, (x + 16, y-30))
    

def enemies(objectX, objectY, objectW, objectH, color):
    """ Prints the enemy image on screen"""
    screen.blit(enemy, (objectX, objectY))
    
def ship(x,y):
    """ Prints the ship image on screen"""
    screen.blit(shipImg, (x,y))

def isCollision(objectX, objectY,bullet_startX,bullet_startY):
    """ Detects if the bullet and enemy are overlapping"""
    distance = math.sqrt((math.pow(objectX-bullet_startX,2)) + (math.pow(objectY-bullet_startY,2)))
    if distance < 200:
        #
        # If over lapping then collision is true
        #
        return True
    else:
        #
        # If over lapping then collision is false
        #
        return False
  
def game_loop(enemySpeed, speed, level):
    """ Main loop where whole game happens"""
    #
    # Creating ship elements
    #
    shipX = 400
    shipY = 476
    x_change = 0

    #
    # Creating all the enemy elements
    #
    object_startX = random.randrange(0,800)
    object_startY = -600
    object_speed = enemySpeed
    object_width = 199
    object_height = 173

    #
    # Creating all the bullet elements
    bulletY_change = 0
    bullet_startX = 0
    bullet_startY = 476
    bullet_speed = 20
    bullet_width = 26
    bullet_height = 36
    bullet_state = False

    #
    # Creates the score text on screen elements
    #
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf',32)
    textX = 10
    textY = 10

    crashed = "no"
    while crashed != "yes":
        #
        # Makes background image
        #
        screen.fill(white)
        screen.blit(background, (0,0))
        for event in pygame.event.get():
                #
                # If you press the x button it quits
                #
                if event.type == pygame.QUIT:
                    crashed = "yes"
                    quit()

                #
                # All main keys and what they do if presses
                #
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -12
                    elif event.key == pygame.K_RIGHT:
                        x_change = +12
                    elif event.key == pygame.K_SPACE:
                        bullet_startX = shipX
                        fire_bullet(bullet_startX,bullet_startY)
                        bullet_state = True
                    
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0

        #
        # Creates enemy and ship movement
        #
        enemies(object_startX, object_startY, object_width, object_height, white)
        object_startY += object_speed
        ship(shipX,shipY)
        shipX += x_change

        #
        # If the ship goes off the screen you lose
        #
        if shipX > 800-53 or shipX < 0:
            crashed = "yes"
            explosion(shipX, shipY -20)

        #
        # deletes enemy if off screen
        #
        if object_startY > 600:
            object_startY = 0 - object_height
            object_startX = random.randrange(0, 800)

        #
        # when bullet goes off screen
        #
        if bullet_startY <= 0:
            bullet_startY = 476
            bullet_state = False

        #
        # detects if the bullet is in the movement state and moves it
        #
        if bullet_state == True:
            fire_bullet(bullet_startX,bullet_startY)
            bullet_startY -= bullet_speed
            
        #
        # All detections if ship hits an enemy (side, top, bottom)
        #
        if shipY < object_startY + object_height:
            if shipX > object_startX and shipX < object_startX + object_width or shipX + 53 > object_startX and shipX + 53 < object_startX + object_width:
                explosion(shipX, shipY+10)
                crashed = "yes"

        #
        # Detects the collission and if a certain collision happens gives you a point
        #
        collision = isCollision(object_startX, object_startY, bullet_startX, bullet_startY)
        if collision:
            bullet_startY = 476
            bullet_state = False
            object_startY = 0 - object_height
            object_startX = random.randrange(0, 800)
            score_value += 1

        #
        # So you don't just do the game or level forever
        #
        if score_value == 20:
            crashed = "yes"

        #
        # prints the score on upper left
        #
        score = font.render(level + " Score : " + str(score_value), True, (white))
        screen.blit(score, (textX,textY))
        
        pygame.display.update()
        clock.tick(speed)

game_loop(8, 100, "Level 1")
game_loop(12, 110, "Level 2")
game_loop(15, 120, "Level 3")
pygame.quit()
quit()


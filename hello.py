import pygame
import time
from datetime import datetime
from datetime import timedelta
import random,sys, copy, os
from pygame.locals import *

SCREEN_WIDTH=600
SCREEN_HEIGHT=600
BLOCK_SIZE = 20
last_turn_time = datetime.now() 
pygame.init()
eatApp=0
total=0

FPSCLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
IMAGESDICT = {'title': pygame.image.load('newstart')}
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

RED=255,0,0
GREEN=0,255,0
BLUE=0,0,255
PURPLE=127,0,127
BLACK=0,0,0
GRAY=127,127,127
WHITE=255,255,255

DIRECTION_ON_KEY = {
    pygame.K_UP: 'north',
    pygame.K_DOWN: 'south',
    pygame.K_LEFT: 'west',
    pygame.K_RIGHT: 'east',
}
block_direction = 'east'
block_position=[0,0]
last_moved_time = datetime.now()
TURN_INTERVAL = timedelta(seconds=0.3)


def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = int(SCREEN_WIDTH / 2)
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['Eat the apple!!!',
                       'Arrow keys to move the snake',
                       'If you go in the opposite direction to the snake, game over..',
                       'if the snake touch its body game over.']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BLACK)

    # Draw the title image to the window:
    DISPLAYSURF.blit(pygame.image.load('start'), titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = pygame.font.Font('freesansbold.ttf', 18).render(instructionText[i], 1, WHITE)
        instRect = instSurf.get_rect()
        topCoord += 10 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = int(SCREEN_WIDTH / 2)
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()
def terminate():
    pygame.quit()
    sys.exit()
def draw_background(screen):
    """draw background."""
    background = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BLACK, background)

def draw_block(screen, color, position):
    """To position draw color block."""
    block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE),
                        (BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, block)
    
class Snake:
    color = GREEN 

    def __init__(self):
        self.positions = [(9, 6), (9, 7), (9, 8), (9, 9)] 
        self.direction = 'north'
    def draw(self, screen):
        i=0;
        for position in self.positions:
            draw_block(screen, (0+i,255-i,0+i), position)
            i=i+5
    def crawl(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'north':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'south':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'west':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'east':
            self.positions = [(y, x + 1)] + self.positions[:-1]
    def turn(self, direction): 
        self.direction = direction
    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'north':
            self.positions.append((y - 1, x))
        elif self.direction == 'south':
            self.positions.append((y + 1, x))
        elif self.direction == 'west':
            self.positions.append((y, x - 1))
        elif self.direction == 'east':
            self.positions.append((y, x + 1))
            
class SnakeCollisionException(Exception):
    pass

class Apple:
    color = RED  

    def __init__(self, position=(5, 5)):
        self.position = position
    def draw(self, screen):
        draw_block(screen, self.color, self.position)
class SecondApp:
    color = RED  

    def __init__(self, position=(7, 2)):
        self.position = position
    def draw(self, screen):
        draw_block(screen, self.color, self.position)

class GameBoard:
    width = 20   
    height = 20
    

    def __init__(self):
        self.snake = Snake() 
        self.apple = Apple()
        self.secondApp=SecondApp()
    def draw(self, screen):
        self.apple.draw(screen)
        self.secondApp.draw(screen)
        self.snake.draw(screen)
        text=BASICFONT.render("How many apple did snake ate? "+str(total), 1, WHITE)
        pos=text.get_rect()
        pos.centerx=150
        screen.blit(text, pos)
    def process_turn(self):
        global eatApp
        global total
        self.snake.crawl()
        if self.snake.positions[0] in self.snake.positions[1:]:
            raise SnakeCollisionException()
        if self.snake.positions[0] == self.apple.position:
            eatApp=eatApp+1
            total=total+1
            self.snake.grow()
            if(eatApp==1):
                self.apple=Apple((-100,-100))
            elif(eatApp!=1):
                eatApp=0
                self.put_new_apple()
                self.put_second_apple()
        elif self.snake.positions[0] == self.secondApp.position:
            eatApp=eatApp+1
            total=total+1
            self.snake.grow()
            if(eatApp==1):
                self.secondApp=SecondApp((-100,-100))
            elif(eatApp!=1):
                eatApp=0
                self.put_new_apple()
                self.put_second_apple()
    def put_new_apple(self):
        self.apple = Apple((random.randint(0, 19), random.randint(0, 19)))  
        for position in self.snake.positions:    
            if self.apple.position == position: 
                self.put_new_apple()
    def put_second_apple(self):
        self.secondApp = SecondApp((random.randint(0, 19), random.randint(0, 19))) 
        for position in self.snake.positions:    
            if self.secondApp.position == position: 
                self.put_second_apple()
                
                break
game_board = GameBoard()
startScreen()
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:  
            if event.key in DIRECTION_ON_KEY:
                game_board.snake.turn(DIRECTION_ON_KEY[event.key])
    if TURN_INTERVAL < datetime.now() - last_turn_time:
        try:
            game_board.process_turn()
        except SnakeCollisionException:
            exit()
        last_turn_time = datetime.now()

    draw_background(screen)
    game_board.draw(screen)
    pygame.display.update()
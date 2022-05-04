# Import the pygame module
from this import d
from xml import dom
import pygame, sys, random
 
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import *

# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4 # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
BLUE =          (  0,  50, 255)
GREEN =         (  0, 128,   0)
RED =           (255,   0,   0)
BGCOLOR = DARKTURQUOISE
TILECOLOR = WHITE
TEXTCOLOR = BLACK
BORDERCOLOR = BLACK
BASICFONTSIZE = 20
SECFONTSIZE = 13
TEXT = GREEN

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global DISPLAYSURF, BASICFONT, SECFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, GAMESIZE

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SECFONT = pygame.font.Font('freesansbold.ttf', SECFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText('Reset',    TEXT, BGCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 310)
    NEW_SURF,   NEW_RECT   = makeText('New Game', TEXT, BGCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 280)
    SOLVE_SURF, SOLVE_RECT = makeText('Solve',    TEXT, BGCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 250)

    GAMESIZE = 3   # 3*3
    drawBoard(GAMESIZE)

    while True:
        checkForQuit()


def gameGenerator(n):
    firstRow = random.sample(range(1,n+1),n)
    permutes = random.sample(range(1,n+1),n)
    return list(firstRow[i:]+firstRow[:i] for i in permutes)



def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def drawTile(tilex, tiley, game, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    # number in the tile
    textSurf = BASICFONT.render(str(game[GAMESIZE-tilex-1][GAMESIZE-tiley-1]), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    # constraint in the top left
    # constSurf = SECFONT.render(str(number), True, TEXTCOLOR)
    # constRect = constSurf.get_rect()
    # constRect.center = left + 11 + adjx, top + 11 + adjy

    pygame.draw.line(DISPLAYSURF, BORDERCOLOR, (left, top),  (left, top + TILESIZE), 3)

    DISPLAYSURF.blit(textSurf, textRect)
    # DISPLAYSURF.blit(constSurf, constRect)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawBoard(n):
    # Generate random game
    game = gameGenerator(n)
    for i in game:
        print(i) 

    DISPLAYSURF.fill(BGCOLOR)
    # if message:
    #     textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
    #     DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(n):
        for tiley in range(n):
            drawTile(tilex, tiley, game)

    # left, top = getLeftTopOfTile(0, 0)
    # width = BOARDWIDTH * TILESIZE
    # height = BOARDHEIGHT * TILESIZE

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    pygame.display.update()





def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        pygame.quit()
        sys.exit() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back




if __name__ == '__main__':
    main()

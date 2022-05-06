# Import the pygame module
import pygame, sys, random
 
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import *

# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 4  # number of columns in the board
BOARDHEIGHT = 4 # number of rows in the board
TILESIZE = 70
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
GREEN =         ( 92, 149,  92)
YELLOW =        (255, 239, 130)
DARKGREEN =     ( 47,  83,  59)
RED =           (255,   0,   0)
BROWN =         (232, 201, 126)
OFFGREEN =      (157, 204, 145)
OFFGREEN2 =     (177, 230, 147)


BGCOLOR = DARKGREEN
TILECOLOR = WHITE
HOVERCOLOR = YELLOW
PRESSCOLOR = OFFGREEN2
TEXTCOLOR = BLACK
BORDERCOLOR = GREEN
BASICFONTSIZE = 20
SECFONTSIZE = 14
TEXT = WHITE

BUTTONCOLOR = WHITE
BUTTONHOVER = OFFGREEN
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
# YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
YMARGIN = 80



def main():
    global DISPLAYSURF, BASICFONT, SECFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, GAMESIZE
    global GAME, CAGES, CONSTRAINTS
    pygame.init()
    GAMESIZE = 4  # n*n
    WINDOWWIDTH = GAMESIZE * TILESIZE + 250
    WINDOWHEIGHT = GAMESIZE * TILESIZE + 200
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Kenken Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SECFONT = pygame.font.Font('freesansbold.ttf', SECFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText(' Reset ',    TEXT, BGCOLOR, 20, 200)
    NEW_SURF,   NEW_RECT   = makeText(' New Game ', TEXT, BGCOLOR, 20, 120)
    SOLVE_SURF, SOLVE_RECT = makeText(' Solve ',    TEXT, BGCOLOR, 20, 160)

    generateNewGame(GAMESIZE)
    drawBoard(GAMESIZE, None, CAGES, CONSTRAINTS)
    
    while True:
        eventHandler()


def gameGenerator(n):
    firstRow = random.sample(range(1,n+1),n)
    permutes = random.sample(range(1,n+1),n)
    return list(firstRow[i:]+firstRow[:i] for i in permutes)


def cagesCreator(game):
    cages=[]
    positions=[]
    for i in range(GAMESIZE):
        for j in range(GAMESIZE):
            positions.append([i+1,j+1])
    while(len(positions) != 0):
        cage=[]
        seed = random.choice(positions)
        cage.append(seed.copy())
        positions.remove(seed)
        # determine how frequent ecah cage size occurs 
        cageSize = random.randint(2,3)
        rand_num = random.randint(1,100)
        if rand_num < 101: cageSize = 4
        if rand_num < 35: cageSize = 3
        if rand_num < 96: cageSize = 3
        if rand_num < 7: cageSize = 1
        

        for i in range(cageSize-1):
            x = seed[0]
            y = seed[1]
            if [x,y+1] in positions: # going right
                seed = [x,y+1]
            elif [x,y-1] in positions: # going left
                seed = [x,y-1]
            elif [x+1,y] in positions: # going dowwn
                seed = [x+1,y]
            elif [x-1,y] in positions: # going up
                seed = [x-1,y]
            else: break
            cage.append(seed.copy())
            positions.remove(seed)
        cages.append(cage)
        
    return cages


def constraintCreator(game,cages):
    constraints =[]
    for cage in cages:
        constraint ={}
        # determine topleft tile and values in the cage
        values=[]
        topleft_tile = cage[0]
        for tile in cage:
            values.append(game[tile[0]-1][tile[1]-1])
            tiley = tile[0]; tilex = tile[1]
            if tiley < topleft_tile[0] or (tiley == topleft_tile[0] and tilex <= topleft_tile[1]):
                topleft_tile = tile
        constraint['topleft'] = topleft_tile

        # pick an arithmetic operation for the cage
        cage_size = len(cage)
        if cage_size == 1:
            op = ' '
        elif cage_size == 2 and max(values[0],values[1]) % min(values[0],values[1]) == 0: 
            op = random.choice(['+','-','÷','x'])
        elif cage_size == 2:
            op = random.choice(['+','-','x'])
        else :
            op = random.choice(['+','x'])
        constraint['op'] = op

        # determine constraint value based on the operation
        cnst = values[0]
        if op=='+':
            cnst = 0
            for v in values: cnst += v 
        elif op=='x':
            cnst = 1
            for v in values: cnst *= v 
        elif op=='-':
            cnst = abs(values[0]-values[1])
        elif op=='÷':
            cnst = int(max(values[0],values[1]) / min(values[0],values[1]))
        constraint['constraint_value'] = cnst
        constraints.append(constraint)
    return constraints


def generateNewGame(n):
    global GAME, CAGES, CONSTRAINTS
    # Generate random game
    GAME = gameGenerator(n)
    # print(game)
    for i in GAME:
        print(i)
    # Create cages for the game
    CAGES = cagesCreator(n)
    print(CAGES)
    # Determine the constraints
    CONSTRAINTS = constraintCreator(GAME, CAGES)
    print(CONSTRAINTS)

def solveGame():
    return GAME   # TO BE CHANGED TO A CSP SOLVER


# Game Draw___________________________________________________________________

global HOVERTILE, PRESSEDTILE, TILES, TILESPOS
HOVERTILE =[]
PRESSEDTILE =[]
TILES =[]
TILESPOS =[]

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def drawTile(tiley, tilex, game, constraint, color, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    tile = pygame.draw.rect(DISPLAYSURF, color, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    global TILES, TILESPOS
    TILESPOS.append([tiley,tilex])
    TILES.append(tile)
    # number in the tile
    if game != None:
        textSurf = BASICFONT.render(str(game[tiley][tilex]), True, TEXTCOLOR)
        textRect = textSurf.get_rect()
        textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
        DISPLAYSURF.blit(textSurf, textRect)
    # constraint in the top left
    if [tiley+1,tilex+1] == constraint['topleft']:
        constSurf = SECFONT.render(str(constraint['constraint_value']) + str(constraint['op']), True, TEXTCOLOR)
        constRect = constSurf.get_rect()
        constRect.center = left + int(constRect.width) -2 + adjx, top + 12 + adjy
        DISPLAYSURF.blit(constSurf, constRect)

global GAMEDISPLAYED
GAMEDISPLAYED = None

def drawBoard(n, game, cages, constraints):
    global HOVERTILE, PRESSEDTILE, TILES, TILESPOS
    DISPLAYSURF.fill(OFFGREEN)
    # if message:
    #     textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
    #     DISPLAYSURF.blit(textSurf, textRect)
    for tiley in range(n):
        for tilex in range(n):
            # constraint = {'topleft':[1,1], 'op':'+', 'constraint_value':3}
            for idx, cage in enumerate(cages):
                if [tiley+1,tilex+1] in cage:
                    constraint = constraints[idx]
                    color = TILECOLOR
                    if [tiley,tilex]==PRESSEDTILE: color = PRESSCOLOR
                    elif [tiley,tilex]==HOVERTILE: color = HOVERCOLOR
                    drawTile(tiley, tilex, game, constraint, color)
    for cage in cages:
        for tile in cage:
            tilex = tile[0]
            tiley = tile[1]
            left, top = getLeftTopOfTile(tiley-1,tilex-1)
            left = left -1
            top = top -1
            if [tilex,tiley-1] not in cage :
                pygame.draw.line(DISPLAYSURF, BORDERCOLOR, (left, top),  (left, top + TILESIZE), 3) #left
            if [tilex-1,tiley] not in cage :
                pygame.draw.line(DISPLAYSURF, BORDERCOLOR, (left, top),  (left + TILESIZE, top), 3) #top
            if [tilex+1,tiley] not in cage :
                pygame.draw.line(DISPLAYSURF, BORDERCOLOR, (left + TILESIZE, top + TILESIZE),  (left , top + TILESIZE), 3) #bottom
            if [tilex,tiley+1] not in cage :
                pygame.draw.line(DISPLAYSURF, BORDERCOLOR, (left + TILESIZE, top + TILESIZE),  (left + TILESIZE , top), 3) #right
                
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    pygame.display.update()



# Game controlers__________________________________________________________

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


global val
val = -1
def eventHandler():
    global HOVERTILE, PRESSEDTILE, TILES, TILESPOS, GAMEDISPLAYED
    global GAMEDISPLAYED, val, PRESSEDTILE
    val = -1
    for event in pygame.event.get():
        ## get position of cursor
        pos = pygame.mouse.get_pos()
        # Handle mouse press events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ## check if cursor is on tile ##
            PRESSEDTILE = []
            if len(TILES) !=0:
                for i in range(len(TILES)):
                    if TILES[i].collidepoint(pos):
                        PRESSEDTILE = TILESPOS[i]
            ## check if cursor is on button ##
            if NEW_RECT.collidepoint(pos):
                # New game
                generateNewGame(GAMESIZE)
                GAMEDISPLAYED = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif SOLVE_RECT.collidepoint(pos):
                # Solve game
                solved = solveGame()
                GAMEDISPLAYED = solved
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif RESET_RECT.collidepoint(pos):
                # Reset game
                GAMEDISPLAYED = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            
        # Handle mouse hover events
        elif event.type == pygame.MOUSEMOTION:
            ## check if cursor is on tile ##
            HOVERTILE = None
            if len(TILES) !=0:
                for i in range(len(TILES)):
                    if TILES[i].collidepoint(pos):
                        HOVERTILE = TILESPOS[i]
            if HOVERTILE != None: drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            ## check if cursor is on button ##
            if NEW_RECT.collidepoint(pos) or \
                    SOLVE_RECT.collidepoint(pos) or \
                    RESET_RECT.collidepoint(pos) :
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return
            else :pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Key handler
        elif event.type == pygame.KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit() # terminate if the KEYUP event was for the Esc key
            # Insert values
            elif event.key == K_KP0: val = 0
            elif event.key == K_KP1: val = 1
            elif event.key == K_KP2: val = 2
            elif event.key == K_KP3: val = 3
            elif event.key == K_KP4: val = 4
            elif event.key == K_KP5: val = 5
            elif event.key == K_KP6: val = 6
            elif event.key == K_KP7: val = 7
            elif event.key == K_KP8: val = 8
            elif event.key == K_KP9: val = 9

            if event.key ==K_RIGHT:
                if len(PRESSEDTILE) !=0 and PRESSEDTILE[1]+1 <= GAMESIZE-1:
                    PRESSEDTILE = [PRESSEDTILE[0], PRESSEDTILE[1]+1]
                    drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            elif event.key ==K_LEFT:
                if len(PRESSEDTILE) !=0 and PRESSEDTILE[1]-1 >= 0:
                    PRESSEDTILE = [PRESSEDTILE[0], PRESSEDTILE[1]-1]
                    drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            elif event.key ==K_UP:
                if len(PRESSEDTILE) !=0 and PRESSEDTILE[0]-1 >= 0:
                    PRESSEDTILE = [PRESSEDTILE[0]-1, PRESSEDTILE[1]]
                    drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            elif event.key ==K_DOWN:
                if len(PRESSEDTILE) !=0 and PRESSEDTILE[0]+1 <= GAMESIZE-1:
                    PRESSEDTILE = [PRESSEDTILE[0]+1, PRESSEDTILE[1]]
                    drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            # pygame.event.post(event) # put the other KEYUP event objects back

        # Check for quit
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # terminate if any QUIT events are present

        # Inseting values
        if val != -1 :
            if GAMEDISPLAYED == None:
                GAMEDISPLAYED = []
                for h in range(GAMESIZE):
                    row = []
                    for v in range(GAMESIZE):
                        row.append('')
                    GAMEDISPLAYED.append(row)
            h = PRESSEDTILE[0]
            v = PRESSEDTILE[1]
            if val == 0: GAMEDISPLAYED[h][v] = ''
            else: GAMEDISPLAYED[h][v] = val
            drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            # print(GAMEDISPLAYED)

        

    # # Check for quit
    # for event in pygame.event.get(QUIT): # get all the QUIT events
    #     pygame.quit()
    #     sys.exit() # terminate if any QUIT events are present
    # for event in pygame.event.get(KEYUP): # get all the KEYUP events
    #     if event.key == K_ESCAPE:
    #         pygame.quit()
    #         sys.exit() # terminate if the KEYUP event was for the Esc key
    #     pygame.event.post(event) # put the other KEYUP event objects back


if __name__ == '__main__':
    main()

#


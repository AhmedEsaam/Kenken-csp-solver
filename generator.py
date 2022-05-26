# Import the pygame module
import pygame, sys, random
 
# Import pygame.locals for easier access to key coordinates
from pygame.locals import *
from new_game import generateNewGame
from solving import solveGame

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
DARKGREY =      ( 55,  58,  64)
OFFGREY =       (238, 238, 238)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
BLUE =          (  0,  50, 255)
GREEN =         ( 92, 149,  92)
YELLOW =        (255, 239, 130)
DARKGREEN =     ( 47,  83,  59)
DARKGREEN2 =    ( 68, 106,  70)
RED =           (255,   0,   0)
BROWN =         (232, 201, 126)
OFFGREEN =      (157, 204, 145)
OFFGREEN2 =     (177, 230, 147)


BGCOLOR = DARKGREEN2
TILECOLOR = WHITE
HOVERCOLOR = YELLOW
PRESSCOLOR = OFFGREEN2
TEXTCOLOR = BLACK
BORDERCOLOR = GREEN
BASICFONTSIZE = 20
SECFONTSIZE = 14
TEXT = OFFGREY

BUTTONCOLOR = BLACK
BUTTONHOVER = OFFGREEN
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
# YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
YMARGIN = 80



def main():
    global DISPLAYSURF, BASICFONT, SECFONT, SECFONT2, SECFONT3, FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, SIZE_SURF, SIZE_RECT, SOL_SURF, SOL_RECT, GAMESIZE
    global GAME, CAGES, CONSTRAINTS
    pygame.init()
    GAMESIZE = 3  # n*n
    WINDOWWIDTH = GAMESIZE * TILESIZE + 250
    WINDOWHEIGHT = GAMESIZE * TILESIZE + 200
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Kenken Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SECFONT = pygame.font.Font('freesansbold.ttf', SECFONTSIZE)
    SECFONT2 = pygame.font.Font(None, SECFONTSIZE + 7)
    SECFONT3 = pygame.font.Font('freesansbold.ttf', SECFONTSIZE-2)
    FONT = BASICFONT

    drawGameOptions()
    GAME, CAGES, CONSTRAINTS = generateNewGame(GAMESIZE)
    drawBoard(GAMESIZE, None, CAGES, CONSTRAINTS)
    
    while True:
        eventHandler()


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
    global DISPLAYSURF, BASICFONT, SECFONT, SECFONT2, FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, SIZE_SURF, SIZE_RECT, SOL_SURF, SOL_RECT, GAMESIZE
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
    
    pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 97     , 127, 24))
    pygame.draw.rect(DISPLAYSURF, OFFGREY,  (0, 97+24  , 127, 96))

    pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 137+80 , 127, 24))
    pygame.draw.rect(DISPLAYSURF, OFFGREY,  (0, 137+80+24 , 127, 96))

    pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 177+160, 127, 24))

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    for x in range(4): DISPLAYSURF.blit(SIZE_SURF[x], SIZE_RECT[x])
    for x in range(3): DISPLAYSURF.blit(SOL_SURF[x], SOL_RECT[x])    
    pygame.display.update()


# Game controlers__________________________________________________________

def makeText(text, color, font, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawGameOptions():
    global DISPLAYSURF, BASICFONT, SECFONT, SECFONT2, FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, SIZE_SURF, SIZE_RECT, SOL_SURF, SOL_RECT, GAMESIZE
    # Store the option buttons and their rectangles in OPTIONS.
    NEW_SURF,   NEW_RECT   = makeText('  New Game ',       TEXT, FONT, 0, 100)
    SOLVE_SURF, SOLVE_RECT = makeText('  Solve         ',  TEXT, FONT, 0, 140+80)
    RESET_SURF, RESET_RECT = makeText('  Reset         ',  TEXT, FONT, 0, 180+160)

    group = buttonGroup(127, SECFONT2)
    SIZE_SURF = []
    SIZE_RECT = []
    for x in range(4):
        group.buttons.append(button(group, str(x+3)+' x '+str(x+3)))
        s_surf, s_rect = group.buttons[x].draw()
        SIZE_SURF.append(s_surf)
        SIZE_RECT.append(s_rect)

    group = buttonGroup(250, SECFONT3)
    SOL_SURF = []
    SOL_RECT = []
    sol_techniques=[]
    sol_techniques.append('Backtracking')
    sol_techniques.append('BT w/ Forward Ch.')
    sol_techniques.append('BT w/ FC & Arc Cons.') 
    for x in range(3):
        group.buttons.append(button(group, sol_techniques[x]))
        s_surf, s_rect = group.buttons[x].draw()
        SOL_SURF.append(s_surf)
        SOL_RECT.append(s_rect)

        
class buttonGroup():
    def __init__(self, start_pos, font):
        self.buttons = []
        self.start_pos = start_pos
        self.font = font

class button():
    # global SIZE_SURF, SIZE_RECT
    def __init__(self,parent,text):
        self.parent = parent
        self.text = text
        self.selected = False

    def select(self):
        for x in self.parent.buttons: x.selected = False
        self.selected = True

    def draw(self):
        SIZE_SURF, SIZE_RECT = makeText(self.text, DARKGREY, self.parent.font, 5, self.parent.start_pos)
        self.parent.start_pos += 22
        return (SIZE_SURF, SIZE_RECT)
        if self.selected: ...
        else: ...
        

global val
val = -1
def eventHandler():
    global GAME, CAGES, CONSTRAINTS, HOVERTILE, PRESSEDTILE, TILES, TILESPOS, GAMEDISPLAYED
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
                GAME, CAGES, CONSTRAINTS = generateNewGame(GAMESIZE)
                GAMEDISPLAYED = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif SOLVE_RECT.collidepoint(pos):
                # Solve game
               # solved = GAME  # comment
            
                solved = solveGame(GAMESIZE, CAGES, CONSTRAINTS, 'BT')
                GAMEDISPLAYED = solved
                print(solved)
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
            elif event.key == K_BACKSPACE: val = 0
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
            if len(PRESSEDTILE) != 0:
                h = PRESSEDTILE[0]
                v = PRESSEDTILE[1]
                if val == 0: GAMEDISPLAYED[h][v] = ''
                else: GAMEDISPLAYED[h][v] = val
                drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            # print(GAMEDISPLAYED)



if __name__ == '__main__':
    main()

##


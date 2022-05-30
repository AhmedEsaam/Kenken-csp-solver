# Import the pygame module
from tokenize import group
import pygame, sys
 
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
GREY =          (115, 119, 123)
OFFGREY =       (238, 238, 238)
GREY1 =         (190, 190, 190)
GREY2 =         (215, 215, 215)
BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
BLUE =          (  0,  50, 255)
GREEN =         ( 92, 149,  92)
YELLOW =        (255, 239, 130)
DARKGREEN =     ( 47,  83,  59)
DARKGREEN2 =    ( 68, 106,  70)
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
BUTTONHOVER = GREY
OPSEL = GREY1
OPHOV = GREY2
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
# YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)
YMARGIN = 80



def main():
    global DISPLAYSURF, BASICFONT, SECFONT, SECFONT2, SECFONT3, FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, SIZE_SURF, SIZE_RECT, SOL_SURF, SOL_RECT, GAMESIZE
    global GAME, CAGES, CONSTRAINTS
    global TECHNIQUE, HEURISTIC
    pygame.init()
    GAMESIZE = 4  # n*n
    TECHNIQUE = 'BT'
    HEURISTIC = 'MCV'
    WINDOWWIDTH = GAMESIZE * TILESIZE + 250
    WINDOWHEIGHT = GAMESIZE * TILESIZE + 200
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Kenken Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    SECFONT = pygame.font.Font('freesansbold.ttf', SECFONTSIZE)
    SECFONT2 = pygame.font.Font(None, SECFONTSIZE + 7)
    SECFONT3 = pygame.font.Font('freesansbold.ttf', SECFONTSIZE-3)
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
    global DISPLAYSURF, BASICFONT, SECFONT, SECFONT2, FONT, sizes_group, sol_group, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, SIZE_SURF, SIZE_RECT, SOL_SURF, SOL_RECT, GAMESIZE
    DISPLAYSURF.fill(OFFGREEN)
    # if message:
    #     textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
    #     DISPLAYSURF.blit(textSurf, textRect)

    # Draw tiles
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
    # Draw tiles' boarders
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
    
    # Draw game controlers
    pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 97     , 127, 24))
    pygame.draw.rect(DISPLAYSURF, OFFGREY,  (0, 97+24  , 127, 102))

    pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 143+80 , 127, 24))
    pygame.draw.rect(DISPLAYSURF, OFFGREY,  (0, 143+80+24 , 127, 96))

    pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 183+160, 127, 24))

    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    for x in range(4): 
        sizes_group.buttons[x].draw()
    for x in range(3):
        sol_group.buttons[x].draw()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    pygame.display.update()


# Game controlers__________________________________________________________

def makeText(text, color, font, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawGameOptions():
    global DISPLAYSURF, BASICFONT, SECFONT, SECFONT2, FONT, sizes_group, sol_group, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT, SIZE_SURF, SIZE_RECT, SOL_SURF, SOL_RECT, GAMESIZE
    # Store the option buttons and their rectangles in OPTIONS.
    NEW_SURF,   NEW_RECT   = makeText('  New Game ',       TEXT, FONT, 0, 100)
    SOLVE_SURF, SOLVE_RECT = makeText('  Solve         ',  TEXT, FONT, 0, 146+80)
    RESET_SURF, RESET_RECT = makeText('  Reset         ',  TEXT, FONT, 0, 186+160)
    
    # Board sizes options 
    sizes_group = buttonGroup(127, SECFONT2)
    SIZE_SURF = []
    SIZE_RECT = []
    for x in range(4):
        sizes_group.buttons.append(button(sizes_group, str(x+3)+' x '+str(x+3)))
        s_surf, s_rect = sizes_group.buttons[x].draw()
        SIZE_SURF.append(s_surf)
        SIZE_RECT.append(s_rect)

    # Solving Techniques options
    sol_group = buttonGroup(252, SECFONT3)
    SOL_SURF = []
    SOL_RECT = []
    sol_techniques=[]
    sol_techniques.append(' Backtracking')
    sol_techniques.append(' BT w/ Forward Check.')
    sol_techniques.append(' BT w/ Arc Consist.') 
    for x in range(3):
        sol_group.buttons.append(button(sol_group, sol_techniques[x]))
        s_surf, s_rect = sol_group.buttons[x].draw()
        SOL_SURF.append(s_surf)
        SOL_RECT.append(s_rect)
        sol_group.buttons[0].select()

class buttonGroup():
    def __init__(self, start_pos, font):
        self.buttons = []
        self.start_pos = start_pos
        self.font = font

class button():
    # global SIZE_SURF, SIZE_RECT
    def __init__(self, parent, text):
        self.parent = parent
        self.text = text
        self.selected = False
        self.s_surf, self.s_rect = makeText(self.text, DARKGREY, self.parent.font, 5, self.parent.start_pos)
        self.pos = self.parent.start_pos
        self.parent.start_pos += 24
        self.draw()

    def select(self):
        for x in self.parent.buttons: x.selected = False
        self.selected = True
        self.draw()

    def draw(self):
        if self.selected:
            rect = pygame.draw.rect(DISPLAYSURF, OPSEL, (0, self.pos-5, 127, 24))
            # DISPLAYSURF.blit(self.s_surf, self.s_rect )    
            pygame.display.update()
        else:
            rect = pygame.draw.rect(DISPLAYSURF, OFFGREY, (0, self.pos-5 , 127, 24))
            # DISPLAYSURF.blit(self.s_surf, self.s_rect )    
            pygame.display.update()
            ...

        DISPLAYSURF.blit(self.s_surf, self.s_rect)
        return (self.s_surf, rect)
    
    def hover(self):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        for x in range(len(sol_group.buttons)):
            sol_group.buttons[x].draw()
        pygame.draw.rect(DISPLAYSURF, OPHOV, (0, self.pos-5 , 127, 24))
        DISPLAYSURF.blit(self.s_surf, self.s_rect)
        pygame.display.update()

    
        
# Event Handler__________________________________________________________

global val
val = -1
def eventHandler():
    global GAME, CAGES, CONSTRAINTS, HOVERTILE, PRESSEDTILE, TILES, TILESPOS, GAMEDISPLAYED
    global GAMEDISPLAYED, val, PRESSEDTILE, sizes_group, sol_group 
    global TECHNIQUE, HEURISTIC
    val = -1
    for event in pygame.event.get():
        ## get position of cursor
        pos = pygame.mouse.get_pos()

        # Handle mouse press events__________________________________________
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            ## check if cursor is on tile ##
            PRESSEDTILE = []
            if len(TILES) !=0:
                for i in range(len(TILES)):
                    if TILES[i].collidepoint(pos):
                        PRESSEDTILE = TILESPOS[i]

            ## check if cursor is on button ##
            #_____New Game and sizes
            if NEW_RECT.collidepoint(pos):
                # New game
                GAME, CAGES, CONSTRAINTS = generateNewGame(GAMESIZE)
                GAMEDISPLAYED = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            #_____Solve and techniques
            # Solve game
            elif SOLVE_RECT.collidepoint(pos):
                # solved = GAME  # comment
                solved, a_ = solveGame(GAMESIZE, CAGES, CONSTRAINTS, TECHNIQUE, HEURISTIC)
                GAMEDISPLAYED = solved
                print(solved)
                print(TECHNIQUE, ' ', HEURISTIC)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # Backtracking
            elif SOL_RECT[0].collidepoint(pos):
                sol_group.buttons[0].select()
                TECHNIQUE = 'BT'
                solved, a_ = solveGame(GAMESIZE, CAGES, CONSTRAINTS, TECHNIQUE, HEURISTIC)
                GAMEDISPLAYED = solved
                print(solved)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # BT with Forward Checking 
            elif SOL_RECT[1].collidepoint(pos):
                sol_group.buttons[1].select()
                TECHNIQUE = 'FC'
                solved, a_ = solveGame(GAMESIZE, CAGES, CONSTRAINTS, TECHNIQUE, HEURISTIC)
                GAMEDISPLAYED = solved
                print(solved)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # BT with Arc Consistency
            elif SOL_RECT[2].collidepoint(pos):
                sol_group.buttons[2].select()
                TECHNIQUE = 'AC'
                solved, a_ = solveGame(GAMESIZE, CAGES, CONSTRAINTS, TECHNIQUE, HEURISTIC)
                GAMEDISPLAYED = solved
                print(solved)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            #_____Reset
            elif RESET_RECT.collidepoint(pos):
                # Reset game
                GAMEDISPLAYED = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            
        # Handle mouse hover events_______________________________________
        elif ((event.type == pygame.MOUSEMOTION) or (event.type == pygame.MOUSEBUTTONUP)):
            ## check if cursor is on tile ##
            HOVERTILE = None
            if len(TILES) !=0:
                for i in range(len(TILES)):
                    if TILES[i].collidepoint(pos):
                        HOVERTILE = TILESPOS[i]
            if HOVERTILE != None: drawBoard(GAMESIZE, GAMEDISPLAYED, CAGES, CONSTRAINTS)
            ## check if cursor is on button ##
            if NEW_RECT.collidepoint(pos):
                pygame.draw.rect(DISPLAYSURF, BUTTONHOVER, (0, 97     , 127, 24))
                DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif SOLVE_RECT.collidepoint(pos):
                pygame.draw.rect(DISPLAYSURF, BUTTONHOVER , (0, 143+80 , 127, 24))
                DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif RESET_RECT.collidepoint(pos):
                pygame.draw.rect(DISPLAYSURF, BUTTONHOVER, (0, 183+160, 127, 24))
                DISPLAYSURF.blit(RESET_SURF, RESET_RECT)   
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
            elif SOL_RECT[0].collidepoint(pos):
                sol_group.buttons[0].hover()
            elif SOL_RECT[1].collidepoint(pos):
                sol_group.buttons[1].hover()
            elif SOL_RECT[2].collidepoint(pos):
                sol_group.buttons[2].hover()
                # return
            else :
                pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 97     , 127, 24))
                pygame.draw.rect(DISPLAYSURF, DARKGREY , (0, 143+80 , 127, 24))
                pygame.draw.rect(DISPLAYSURF, DARKGREY, (0, 183+160, 127, 24))
                DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
                DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)
                DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
                # for x in range(4): 
                #     sizes_group.buttons[x].draw()
                # for x in range(3):
                #     sol_group.buttons[x].draw()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.update()

        # Key handler______________________________________________________
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

        # Check for quit________________________________________
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # terminate if any QUIT events are present

        # Inseting values_______________________________________
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


import random
global GAMESIZE  # n

def gameGenerator(n):
    firstRow = random.sample(range(1,n+1),n)
    permutes = random.sample(range(1,n+1),n)
    return list(firstRow[i:]+firstRow[:i] for i in permutes)


def cagesCreator(GAMESIZE):
    cages=[]
    positions=[]
    for i in range(1,GAMESIZE+1):
        for j in range(1,GAMESIZE+1):
            positions.append([i,j])
    while(len(positions) != 0):
        cage=[]
        seed = random.choice(positions)
        cage.append(seed.copy())
        positions.remove(seed)
        # determine how frequent ecah cage size occurs 
        cageSize = random.randint(2,4)
        if GAMESIZE > 5:
            rand_num = random.randint(1,100)
            if rand_num < 25: cageSize = 1
            elif rand_num < 70: cageSize = 2
            # if rand_num < 55: cageSize = 2
            elif rand_num < 90: cageSize = 3
        
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

def hasMultipleSol(cages, GAMESIZE):  # Check if current cages distribution has multiple solutions
    # Check common columns and rows in cages 
    cols=[]  # left column number of every side-by-side horizontally two tiles in the same cage
    rows=[]  # upper row number of every side-by-side vertically two tiles in the same cage
    n_sized_vertical_cages = 0  #    n stands for Game size
    n_sized_horizontal_cages = 0  
    for cage in cages:
        same_col = 0
        same_row = 0
        for tile in cage:
            h = tile[0]
            v = tile[1]
            if [h, v+1] in cage:
                cols.append(v)
                same_row += 1
            if [h+1, v] in cage:
                rows.append(h)
                same_col += 1
        if same_col == GAMESIZE-1: n_sized_vertical_cages += 1
        if same_row == GAMESIZE-1: n_sized_horizontal_cages += 1

    for i in range(1,GAMESIZE+1):
        if (cols.count(i) == GAMESIZE) or (rows.count(i) == GAMESIZE):
            return 1
    # Check if there exist more than one vertical cages same size as game size,
    #  the same goes for horizontal cages
    if (n_sized_vertical_cages > 1) or (n_sized_horizontal_cages > 1):
        return 1

    return 0


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
    # Generate random game
    GAME = gameGenerator(n)
    # print(game)
    for i in GAME:
        print(i)
    # Create cages for the game
    CAGES = cagesCreator(n)
    while hasMultipleSol(CAGES, n):
        CAGES = cagesCreator(n)
    print(CAGES)
    # Determine the constraints
    CONSTRAINTS = constraintCreator(GAME, CAGES)
    print(CONSTRAINTS)
    return GAME, CAGES, CONSTRAINTS
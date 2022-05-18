def solveGame(GAMESIZE, CAGES, CONSTRAINTS, technique): # TO BE CHANGED TO A CSP SOLVER
    # GAMESIZE : n 

    '''
    if the game size was (3*3) and solution was :
        [2, 3, 1]
        [1, 2, 3]
        [3, 1, 2]

    (CAGES) includes the (row,col) indices of squares in each cage.
        A CAGES distribution might be:

        [[[3, 1], [3, 2], [3, 3], [2, 3]],
         [[2, 2], [2, 1], [1, 1]],
         [[1, 3], [1, 2]]]

    (CONSTRAINTS) includes the operation used in each cage (+,-,x,÷), the constraint value,
        and the most top left square in each cage which is irrelevant in this function context
        - top left square becomes handy when displaying the board only- 
        an example of CONSTRAINTS might be:
        
        [{'topleft': [2, 3], 'op': 'x', 'constraint_value': 18},
         {'topleft': [1, 1], 'op': 'x', 'constraint_value': 4},
         {'topleft': [1, 2], 'op': '+', 'constraint_value': 4}]
    
    '''

    return solved  # TO BE CHANGED TO A CSP SOLVER

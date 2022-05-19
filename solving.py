import random
global GAMESIZE, CAGES, CONSTRAINTS, technique ,square_domains
global row , col
row = 0
col = 0
def CSP_BACKTRACKING(Assignment):
    
    #complete assignment checking
    global GAMESIZE, CAGES, CONSTRAINTS, technique ,square_domains
    global row , col
    size = GAMESIZE 
    valid_Assignment = True
    complete_Assignment = True
    for i in Assignment:
        for j in i:
            if(j==0):
                complete_Assignment = False  
    
    if(complete_Assignment):
        return Assignment
    
    #assign value from square domains
    print(square_domains[row][col])
    random.shuffle(square_domains[row][col])
    print(square_domains[row][col])
    for v in square_domains[row][col] :
        Assignment[row][col] = v
        print(v)
        valid_Assignment = True
        #valid assignment checking
        for i in range(size) : 
            if( (Assignment[row][i]==Assignment[row][col]) and (i != col) ):
                valid_Assignment = False
                print("i= ",i ,"valid_Assignment =  " ,valid_Assignment )
            if( (Assignment[i][col]==Assignment[row][col]) and (i != row) ):
                valid_Assignment = False
                print("i= ",i ,"valid_Assignment =  " ,valid_Assignment )
            #...
        if(valid_Assignment ): 
            print("valid")
            if(col != size-1):
                col +=1 
            else:
                row += 1 
                col = 0 
        
            result = CSP_BACKTRACKING(Assignment)
            if(result == 'failure') :
                print("enter")
                Assignment = [[0 for i in range(size)] for j in range(size)]
                result = CSP_BACKTRACKING(Assignment)
            else :
                return result

        #else if(!valid_Assignment)  assign another value from square domains  by next iteration 
    return 'failure'          

def solveGame(GAMESIZE_, CAGES_, CONSTRAINTS_, technique_): # TO BE CHANGED TO A CSP SOLVER
    global GAMESIZE, CAGES, CONSTRAINTS, technique,square_domains
    GAMESIZE = GAMESIZE_
    CAGES = CAGES_
    CONSTRAINTS = CONSTRAINTS_
    technique  = technique_
    '''
    (GAMESIZE) : is the side size of the game
        if the game size was (3*3) then GAMESIZE = 3, and solution might be :

        [[2, 3, 1],
         [1, 2, 3],
         [3, 1, 2]]

    (CAGES) : includes the (row,col) indices of squares in each cage.
        A CAGES distribution might be:

        [[[3, 1], [3, 2], [3, 3], [2, 3]],
         [[2, 2], [2, 1], [1, 1]],
         [[1, 3], [1, 2]]]

    (CONSTRAINTS) : includes the operation used in each cage (+,-,x,÷), the constraint value,
        and the most top left square in each cage which is irrelevant in this function context
        - top left square becomes handy when displaying the board only- 
        an example of CONSTRAINTS might be:

        [{'topleft': [2, 3], 'op': 'x', 'constraint_value': 18},
         {'topleft': [1, 1], 'op': 'x', 'constraint_value': 4},
         {'topleft': [1, 2], 'op': '+', 'constraint_value': 4}]

    (technique) : is a string value of the solving technique used one of ('BT', 'FC', 'AC')

        'BT' : Backtracking
        'FC' : Backtracking with forward checking
        'AC' : Backtracking with forward checking and arc consistency
    
    '''
    


    size = GAMESIZE
    rows, cols = (size, size)

    # initialize vars domains [1:size]
    square_domains = [[[i+1 for i in range(rows)] for j in range(cols)] for k in range(size)]
    # print(square_domains)

    # Empty Assignment : initialize Assignment by zero 
    
    Assignment = [[0 for i in range(size)] for j in range(rows)]
    
    return CSP_BACKTRACKING(Assignment)
    #print(Assignment)

# initialize square value
# square_value = [[0 for i in range(rows)] for j in range(cols)]

# BACKTRACKING  function

 


           
Assignment =  solveGame(3, 0, 0, 0)                 
print('Assignment : ' ,Assignment)   





 #Hello
from asyncio.windows_events import NULL
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
    # print(square_domains[row][col])
    random.shuffle(square_domains[row][col])
    #print(square_domains[row][col])
    for v in square_domains[row][col] :
        Assignment[row][col] = v
        print("------------------------------------")
        print(v)
        print("------------------------------------")
        valid_Assignment = True
        #valid assignment checking
        for i in range(size) : 
            # validate over the row and col
            if( (Assignment[row][i]==Assignment[row][col]) and (i != col) ):
                valid_Assignment = False
                #print("i= ",i ,"valid_Assignment =  " ,valid_Assignment )
            if( (Assignment[i][col]==Assignment[row][col]) and (i != row) ):
                valid_Assignment = False
                #print("i= ",i ,"valid_Assignment =  " ,valid_Assignment )
            # validate over the cage constraint
            flag=0
            idx_=0
            res=0
            cage_vals=[] 
            for idx,cage in enumerate(CAGES) :
                if([row+1 ,col+1] in cage) :
                    print("there --------")
                    print(cage)
                    idx_=idx
                    for cell in cage :
                        val=Assignment[cell[0]-1][cell[1]-1]
                        cage_vals.append(val)
                        #print("ffsfsfs............")
                        if(val == 0):
                            flag=1
                            print("here------------------------------------")
                            print(Assignment[cell[0]-1][cell[1]-1])
            
            if (flag==0) :
                constraint=CONSTRAINTS[idx_]
                op=constraint['op']
                constraint_value=constraint['constraint_value']
                if(op == '+') :
                    for item in cage_vals:
                        res=res+item
                if(op == 'x') :
                    res=1
                    for item in cage_vals:
                        res=res*item
                if(op == '-') :
                    for item in cage_vals:
                        res=abs(cage_vals[0]-cage_vals[1])
                if(op == '÷') :
                    for item in cage_vals:
                        res=max(cage_vals)/min(cage_vals)

                if(res != constraint_value) :
                    valid_Assignment = False

                            

            
            
            #...
        if(valid_Assignment ): 
            print("valid")
            print(Assignment)
            if(col != size-1):
                col +=1 
            else:  #row != size-1
                row += 1 
                col = 0 
        
            result = CSP_BACKTRACKING(Assignment)
            if(result == 'failure') :
                row = 0
                col = 0
                #print("enter")
                Assignment = [[0 for i in range(size)] for j in range(size)]
                result = CSP_BACKTRACKING(Assignment)
            else :
                return result

        #else if(!valid_Assignment)  assign another value from square domains  by next iteration 
    return 'failure'

def solveGame(GAMESIZE_, CAGES_, CONSTRAINTS_, technique_): # TO BE CHANGED TO A CSP SOLVER
    global GAMESIZE, CAGES, CONSTRAINTS, technique,square_domains
    global row , col
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
    row = 0
    col = 0
    csp_BT = CSP_BACKTRACKING(Assignment)
    #print('Assignment : ' ,csp_BT)   
    return csp_BT
    #print(Assignment)

# initialize square value
# square_value = [[0 for i in range(rows)] for j in range(cols)]

# BACKTRACKING  function

 


           
# Assignment =  solveGame(3, [[[3, 1], [3, 2]], [[2, 3], [2, 2]], [[2, 1], [1, 1], [1, 2], [1, 3]], [[3, 3]]] , [{'topleft': [3, 1], 'op': 'x', 'constraint_value': 3}, {'topleft': [2, 2], 'op': 'x', 'constraint_value': 6}, {'topleft': [1, 1], 'op': 'x', 'constraint_value': 6}, {'topleft': [3, 3], 'op': ' ', 'constraint_value': 2}], 0)                 
# print('Assignment : ' ,Assignment)   





 #Hello
    #HHHH

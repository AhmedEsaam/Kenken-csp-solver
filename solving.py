from asyncio.windows_events import NULL
import random
global GAMESIZE, CAGES, CONSTRAINTS, technique ,square_domains
global row , col
global cages_h
global cell_index
def forward_checking( domains, x , v, op, constraint_value, idx_, cell_idx_, res, Assignment):
    global GAMESIZE 
    for i in range(GAMESIZE) : 
        # validate over the row and col
        if (i != col) :
            
            if v in square_domains[row][i] :
               square_domains[row][i].remove(v) 
            
            
        if (i != row) :
            if v in square_domains[i][col] : 
               square_domains[i][col].remove(v)

    # change domains of cells in same cage
    # '''
    cage = CAGES[idx_]
    cnst_v = constraint_value
    # print('op :', op)
    # print('cage:', cage)
    # print(x)
    for cell in cage:
        row_next = cell[0]-1
        col_next = cell[1]-1
        if ((row != row_next) or (col != col_next)) :
            
            if (op == '-'):
                if (v - cnst_v > 0):
                    next_domain = []
                    if ((v - cnst_v) in domains[row_next][col_next]) :
                        next_domain.append(v - cnst_v)
                    if ((v + cnst_v) in domains[row_next][col_next]) :
                        next_domain.append(v + cnst_v)
                    domains[row_next][col_next] = next_domain
                elif (v - cnst_v < 0):
                    if ((v + cnst_v) in domains[row_next][col_next]) :
                        domains[row_next][col_next] = [v + cnst_v]
                else:
                    domains[row_next][col_next] = []

            if (op == '÷'):
                next_domain = []
                if (int(v / cnst_v) in domains[row_next][col_next]) :
                    next_domain.append(int(v / cnst_v))
                if ((v * cnst_v) in domains[row_next][col_next]) :
                    next_domain.append(v * cnst_v)
                domains[row_next][col_next] = next_domain

    return square_domains        




def CSP_BACKTRACKING(Assignment):
    #complete assignment checking
    global GAMESIZE, CAGES, CONSTRAINTS, technique ,square_domains
    global row , col
    global cages_h
    global cell_index
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
        # print("------------------------------------")
        # print(v)
        # print("------------------------------------")
        valid_Assignment = True
        #valid assignment checking
        if technique == "BT" :
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
                    # print("there --------")
                    # print(cage)
                    idx_=idx
                    for cell in cage :
                        val=Assignment[cell[0]-1][cell[1]-1]
                        cage_vals.append(val)
                        #print("ffsfsfs............")

                        if(val == 0):
                            flag=1
                            # print("here------------------------------------")
                            # print(Assignment[cell[0]-1][cell[1]-1])
            
            if (flag==0) :
                constraint=CONSTRAINTS[idx_]
                op=constraint['op']
                constraint_value=constraint['constraint_value']
                if(op == '+') :
                    res=0
                    res=sum(cage_vals)
                elif(op == 'x') :
                    res=1
                    for item in cage_vals:
                        res = res * item
                elif(op == '-') :
                        res=abs(cage_vals[0]-cage_vals[1])
                elif(op == '÷') :
                        res=max(cage_vals)/min(cage_vals)
                else:
                    res=0
                    res=sum(cage_vals)
                if(res != int(constraint_value)) :
                    valid_Assignment = False
                # else :
                #     print("TRUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    ## OUTPUT Trial--------------------------------------
                # print('op : ' , op)
                # print('constraint value : ' , constraint_value)
                # print('result : ',res)
                # print('valid_Assignment :' , valid_Assignment)
                # print('cage :' , cage_vals)

            
        elif (technique=="FC"): 
            x = [row,col]
            print(square_domains)
            domains = forward_checking(square_domains, x , v, Assignment)
            square_domains = domains
            for row_ in square_domains:
                for domain in row_ :
                    if domain == [] :
                        valid_Assignment = False 
                        


        if(valid_Assignment == True):
                print("valid")
                print(Assignment)
                # if(col != size-1):
                #     col +=1 
                # else:  #row != size-1
                #     row += 1 
                #     col = 0 
                if(cell_index < (size*size)-1):
                    cell_index += 1
                    row =cages_h[cell_index][0]-1
                    print('rowwwwwww',row)
                    col =cages_h[cell_index][1]-1 
            
                result = CSP_BACKTRACKING(Assignment)
                # if(result != 'failure') :
                #     # row = 0
                #     # col = 0
                #     result = CSP_BACKTRACKING(Assignment)
                #     return result
                #     #print("enter")
                #     Assignment = [[0 for i in range(size)] for j in range(size)]
                #     result = CSP_BACKTRACKING(Assignment)
                # else :
                return result
         
    # print('failure')
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

    ## for least constrained heurstic
    global cages_h
    global cell_index
    
    cell_index=0
    cages_h=CAGES.copy()
    cages_h.sort(key = len)
    temp=[]
    for cage in cages_h :
        for cell in cage :
            temp.append(cell)  
    cages_h=temp
        

    # initialize vars domains [1:size]
    
    # print(square_domains)

    # Empty Assignment : initialize Assignment by zero 
    
    # Assignment = [[0 for i in range(size)] for j in range(rows)]
    # # row = 0
    # # col = 0
    # cell_index=0
    # row =cages_h[cell_index][0]-1
    # col =cages_h[cell_index][1]-1
    # csp_BT = CSP_BACKTRACKING(Assignment)
    while(True) :
                    square_domains = [[[i+1 for i in range(rows)] for j in range(cols)] for k in range(size)]
                    Assignment = [[0 for i in range(size)] for j in range(rows)]
                    cell_index=0
                    row =cages_h[cell_index][0]-1
                    col =cages_h[cell_index][1]-1
                    # row=0
                    # col=0
                    #print("enter")
                    csp_BT = CSP_BACKTRACKING(Assignment)
                    if(csp_BT != 'failure') :
                        break


    #print('Assignment : ' ,csp_BT)   
    return csp_BT
    #print(Assignment)

# initialize square value
# square_value = [[0 for i in range(rows)] for j in range(cols)]

# BACKTRACKING  function

 


           
# Assignment =  solveGame(3, [[[3, 1], [3, 2]], [[2, 3], [2, 2]], [[2, 1], [1, 1], [1, 2], [1, 3]], [[3, 3]]] , [{'topleft': [3, 1], 'op': 'x', 'constraint_value': 3}, {'topleft': [2, 2], 'op': 'x', 'constraint_value': 6}, {'topleft': [1, 1], 'op': 'x', 'constraint_value': 6}, {'topleft': [3, 3], 'op': ' ', 'constraint_value': 2}], 0)                 
# print('Assignment : ' ,Assignment)   

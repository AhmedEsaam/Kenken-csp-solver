from asyncio.windows_events import NULL
import random
global GAMESIZE, CAGES, CONSTRAINTS, technique #,square_domains
global row , col
global cages_h
global cell_index
global evaluate


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

def forward_checking( domains, x , v, op, constraint_value, idx_, cell_idx, res, Assignment):
    global GAMESIZE, CAGES
    # change domains of cells in same row and col
    row = x[0]
    col = x[1]
    for i in range(GAMESIZE) : 
            if v in domains[row][i] :
               domains[row][i].remove(v) 
            if v in domains[i][col] : 
               domains[i][col].remove(v) 

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

            if res > 0 : 
                if (op == 'x'):
                    next_domain = domains[row_next][col_next]
                    for d in next_domain:
                        if (d > (cnst_v / res)):
                            next_domain.remove(d)
                    domains[row_next][col_next] = next_domain

                if (op == '+'):
                    next_domain = domains[row_next][col_next]
                    for d in next_domain:
                        if (d > (cnst_v - res)):
                            next_domain.remove(d)
                    domains[row_next][col_next] = next_domain
                    
    # '''   
    return domains  
   

def CSP_BACKTRACKING(Assignment, square_domains):
    global evaluate
    global GAMESIZE, CAGES, CONSTRAINTS, technique #,square_domains
    global row , col
    global cages_h
    global cell_index
    size = GAMESIZE 
    valid_Assignment = True
    complete_Assignment = True
    
    #complete assignment checking
    for i in Assignment:
        for j in i:
            if(j==0):
                complete_Assignment = False  
    
    if(complete_Assignment):
        return Assignment
    
    #assign value from square domains
    random.shuffle(square_domains[row][col])

    #domain_before store the domain before being changed
    domain_before = square_domains.copy()

    for v in square_domains[row][col] :
        #evaluate according to number of values being tried
        evaluate+=1

        #restore the original domain before it has been changed (at this value).
        #Note : the domain is not completely reseted it just restored to what it was at this variable.
        square_domains = domain_before.copy()

        #assign random value v from the domain
        Assignment[row][col] = v
        
        #initialize the valid_Assignment to true (until the opposite is proved)
        valid_Assignment = True

        #valid assignment checking ---------------------------------------------------------------------------------------------
        for i in range(size) : 
            # validate over the row and col
            if( (Assignment[row][i]==Assignment[row][col]) and (i != col) ):
                valid_Assignment = False
            if( (Assignment[i][col]==Assignment[row][col]) and (i != row) ):
                valid_Assignment = False

        #validate over the cage constraint -------------------------------------------------------------------------------------
        if(valid_Assignment == True):
            flag=0
            idx_=0
            cell_idx = 0
            res=0
            cage_vals=[] 

            #append values in this cage to cage_vals to be calculated .
            # if there is zero value then valid assignment is true as it hasn't been finished yet (flag =1)
            # if there is no zero value then the cage is full and we should calculate its value and check the constrain
            for idx,cage in enumerate(CAGES) :
                if([row+1 ,col+1] in cage) :
                    idx_=idx
                    for c_idx, cell in enumerate(cage) :
                        val=Assignment[cell[0]-1][cell[1]-1]
                        cage_vals.append(val)
                        if ((row+1 == cell[0]) and (col+1 == cell[0])):
                            cell_idx = c_idx
                        if(val == 0):
                            flag=1

            #registering the value of cage constraint and its operation to check the constraint
            constraint=CONSTRAINTS[idx_]
            op=constraint['op']
            constraint_value=constraint['constraint_value']
            res = 0

            #check the cage constrain
            if (flag==0) :
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
            
            #Optional if you need Forward Checking :
            if (technique=="FC" and valid_Assignment == True): 
                x = [row,col]
                domains = forward_checking(square_domains, x , v, op, constraint_value, idx_, cell_idx, res, Assignment)
                square_domains = domains
                
                #check if the modified domains has zero domain at any variable AND this variable has not been assigned yet .
                for row_ in domains:
                    for domain in row_ :
                        ##############################################
                        if (domain == [] ) and 1:
                            valid_Assignment == False
                    

        #Check valid_Assignment (all constraints except if the cage is not full assign true) -------------------------------------------------------------------------
        if(valid_Assignment == True):
                #call next index (according to least constraint heurstic)
                if(cell_index < (size*size)-1):
                    cell_index += 1
                    row =cages_h[cell_index][0]-1
                    col =cages_h[cell_index][1]-1 

                #make the same process for the next variable
                result = CSP_BACKTRACKING(Assignment, square_domains)

                #if no failure happens return result else look for another value v in squared domain
                if result !=  'failure':
                    return result
    #the failure indicate termination of this process so we have to get back to the root of recursion and try different values
    print('failure')
    return 'failure'

def solveGame(GAMESIZE_, CAGES_, CONSTRAINTS_, technique_): # TO BE CHANGED TO A CSP SOLVER
    global GAMESIZE, CAGES, CONSTRAINTS, technique#, square_domains
    global row , col
    global evaluate

    GAMESIZE = GAMESIZE_
    CAGES = CAGES_
    CONSTRAINTS = CONSTRAINTS_
    technique  = technique_
    

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
        
    evaluate=0
    while(True) :
        square_domains = [[[i+1 for i in range(rows)] for j in range(cols)] for k in range(size)]
        for idx, cage in enumerate(CAGES):
            if CONSTRAINTS[idx]['op'] == ' ':
                row__ =  CONSTRAINTS[idx]['topleft'][0] -1
                col__ =  CONSTRAINTS[idx]['topleft'][1] -1
                square_domains[row__][col__] = [CONSTRAINTS[idx]['constraint_value']]

        Assignment = [[0 for i in range(size)] for j in range(rows)]
        cell_index=0
        row =cages_h[cell_index][0]-1
        col =cages_h[cell_index][1]-1
        csp_BT = CSP_BACKTRACKING(Assignment, square_domains)
        # print(csp_BT)
        if(csp_BT != 'failure') :
            break 
    print(evaluate)
    return csp_BT

 


           
# Assignment =  solveGame(3, [[[3, 1], [3, 2]], [[2, 3], [2, 2]], [[2, 1], [1, 1], [1, 2], [1, 3]], [[3, 3]]] , [{'topleft': [3, 1], 'op': 'x', 'constraint_value': 3}, {'topleft': [2, 2], 'op': 'x', 'constraint_value': 6}, {'topleft': [1, 1], 'op': 'x', 'constraint_value': 6}, {'topleft': [3, 3], 'op': ' ', 'constraint_value': 2}], 0)                 
# print('Assignment : ' ,Assignment)   


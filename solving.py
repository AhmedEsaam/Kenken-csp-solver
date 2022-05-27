from asyncio.windows_events import NULL
import queue
import random
from xmlrpc.client import INVALID_XMLRPC

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

def forward_checking( domains, x , v, op, constraint_value, idx_, cell_idx_, res , cage_vals, Assignment):
    global GAMESIZE, CAGES
    global evaluate

    if(res==-1):
        return domains

    #this is for certain process where there is x , + 
    #it tries to find out if the remaining is only one value so that we can calculate the next domain which will be only one value
    c=cell_idx_
    if(len(c)) :
        c1=cell_idx_[0]-1
        c2=cell_idx_[1]-1
    
    # change domains of cells in same row and col
    row = x[0]
    col = x[1]
    for i in range(GAMESIZE) : 
        if (i != col) :
            if v in domains[row][i] :
               domains[row][i].remove(v) 
        if (i != row) :
            if v in domains[i][col] : 
               domains[i][col].remove(v)

    # change domains of cells in same cage
    cage = CAGES[idx_]
    cnst_v = constraint_value

    for cell in cage:
        row_next = cell[0]-1
        col_next = cell[1]-1

        #only accept the other cells (not the current one) .
        if ((row != row_next) or (col != col_next)) :
            if (op == '-'):
                next_domain = []

                #initially there is no domain , then we append the value that can be used in any order to get the constraint value
                if (v - cnst_v > 0):
                    if ((v - cnst_v) in domains[row_next][col_next]) :
                        next_domain.append(v - cnst_v)
                    if ((v + cnst_v) in domains[row_next][col_next]) :
                        next_domain.append(v + cnst_v)

                elif (v - cnst_v < 0):
                    if ((v + cnst_v) in domains[row_next][col_next]) :
                        next_domain = [v + cnst_v]
                domains[row_next][col_next] = next_domain

            elif (op == '÷'):
                next_domain = []

                #initially there is no domain , then we append the value that can be used in any order to get the constraint value
                if (int(v / cnst_v) in domains[row_next][col_next]) :
                    next_domain.append(int(v / cnst_v))
                if ((v * cnst_v) in domains[row_next][col_next]) :
                    next_domain.append(v * cnst_v)
                domains[row_next][col_next] = next_domain

            #we needed it at the begining but now this is trivial but just we use it for readability purpose
            if res > 0 : 
                if (op == 'x'):
                    next_domain = domains[row_next][col_next]
                    #if the remaining is only one value then calculate this one value and put in it the needed domain
                    if(len(c)) :
                        if(row_next == c1 and col_next == c2):
                            if( (int(cnst_v/res) in next_domain)) :
                                next_domain = [int(cnst_v/res)]
                            else :
                                next_domain = []
                    
                    #else , add all possible values
                    else :
                        next_domain_ = next_domain.copy()
                        for d in next_domain_:
                            if (d > (cnst_v / res)):
                                    next_domain.remove(d)
                            elif ( ((cnst_v / res)% d) != 0) and (d != 1) :
                                    next_domain.remove(d)
                                
                    domains[row_next][col_next] = next_domain


                if (op == '+'):
                    next_domain = domains[row_next][col_next]
                    #if the remaining is only one value then calculate this one value and put in it the needed domain
                    if(len(c)) :
                        if(row_next == c1 and col_next == c2):
                            if( (cnst_v-res) in next_domain ) :
                                next_domain = [cnst_v-res]
                            else :
                                next_domain = []

                    #else , add all possible values
                    else:
                        next_domain_ = next_domain.copy()
                        for d in next_domain_:
                            if (d > (cnst_v - res)):
                                next_domain.remove(d)
                    domains[row_next][col_next] = next_domain
    return domains  

def REMOVE_INCONSISTENT_VALUES(xi,xj,domains):
    removed=False
    xi_r=xi[0]-1
    xi_c=xi[1]-1
    xj_r=xj[0]-1
    xj_c=xj[1]-1
    op=''
    constraint_value=0
    same_2_sized_cage=0
    for idx,cage in enumerate(CAGES) :
        if([xi_r+1,xi_c+1] in cage) and ([xj_r+1,xj_c+1] in cage) and len(cage)==2  :
            op=CONSTRAINTS[idx]['op']
            constraint_value=CONSTRAINTS[idx]['constraint_value']
            same_2_sized_cage=1

    satisfied=0
    for v in domains[xi_r][xi_c]:
        for u in domains[xj_r][xj_c]:
            if u !=v:
                satisfied=1
            if same_2_sized_cage==1:
                if op=='+':
                    if u+v==constraint_value:
                        satisfied=1
                elif op=='-':
                    if abs(u-v)==constraint_value:
                        satisfied=1
                elif op=='x':
                    if u*v==constraint_value:
                        satisfied=1
                elif op=='÷':
                    if int(max(u,v)/min(u,v))==constraint_value:
                        satisfied=1
                
        if satisfied==0:
            domains[xi_r][xi_c].remove(v)
            removed=True

    return removed,domains


def arc_consistency(domains, x , v, op, constraint_value, idx_, cell_idx_, res, Assignment):
    global neighbors
    X1=[1,1]
    X2=[1,2]
    queue_ =[(X1,X2),(X2,X1)]
    while queue_ !=[]:
        (Xi,Xj)=queue_.pop()
        Xi_r=Xi[0]-1
        Xi_c=Xi[1]-1
        removed,domains=REMOVE_INCONSISTENT_VALUES(Xi, Xj,domains)
        if removed:
            if len(domains[Xi_r][Xi_c])==0:
                return False,domains
            for xk in neighbors[Xi_r][Xi_c]:
                if xk!=Xj:
                    if (xk,Xi) not in queue_:
                        queue_.append((xk,Xi))
    return True,domains


  
   

def CSP_BACKTRACKING(Assignment, square_domains):
    global evaluate
    global GAMESIZE, CAGES, CONSTRAINTS, technique #,square_domains
    global row , col
    global cages_h
    global cell_index
    global neighbors
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
    #########################
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
            cell_idx = []
            res=0
            cage_vals=[] 
            #append values in this cage to cage_vals to be calculated .
            # if there is zero value then valid assignment is true as it hasn't been finished yet (flag =1)
            # if there is no zero value then the cage is full and we should calculate its value and check the constrain
            for idx,cage in enumerate(CAGES) :
                if([row+1 ,col+1] in cage) :
                    idx_=idx
                    for cell in (cage) :
                        val=Assignment[cell[0]-1][cell[1]-1]
                        if val != 0: 
                            cage_vals.append(val)
                        else: 
                            cell_idx = cell
                        if(val == 0):
                            flag=1
                            
            #registering the value of cage constraint and its operation to check the constraint
            constraint=CONSTRAINTS[idx_]
            op=constraint['op']
            constraint_value=constraint['constraint_value']
            cell_idx_ = []
            if (len(CAGES[idx_]) - len(cage_vals) == 1 ) :
                cell_idx_ = cell_idx
            
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
                
                #this is a condition made so that the value of result is not bigger than the cage
                if(op == '+') :
                    res=0
                    res=sum(cage_vals)
                    if( res > constraint_value):
                        valid_Assignment=False
                        res=-1
                elif(op == 'x') :
                    res=1
                    for item in cage_vals:
                        res = res * item
                    if( res > constraint_value):
                        valid_Assignment=False
                        res =-1

                x = [row,col]
                #modify on the other affected domains
                domains = forward_checking(square_domains, x , v, op, constraint_value, idx_, cell_idx_, res,cage_vals, Assignment)
                square_domains = domains 
                
                #check if the modified domains has zero domain at any variable AND this variable has not been assigned yet .
                br =0
                for i in range(GAMESIZE) : 
                    for j in range (GAMESIZE) :
                        if (len(domains[i][j]) == 0) and (Assignment[i][j] == 0) :
                            valid_Assignment == False
                            br=1
                            break
                    if(br==1):
                        break
            
            elif (technique=="AC" and valid_Assignment == True):
                x = [row,col]
                consistency,square_domains = arc_consistency(square_domains, x , v, op, constraint_value, idx_, cell_idx_, res, Assignment)
                if not consistency:
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
    global neighbors
    cell_index=0
    cages_h=CAGES.copy()
    cages_h.sort(key = len)
    temp=[]
    for cage in cages_h :
        for cell in cage :
            temp.append(cell)  
    cages_h=temp
        
    evaluate=0
    Possibilities=(GAMESIZE)**(GAMESIZE**2) #Possibilities of all boards
    neighbors =[[[] for j in range(cols)] for k in range(size)]
    for r in range(GAMESIZE):
        for c in range(GAMESIZE):
            for n in range(GAMESIZE):
                if (n!=c) and (n!=r):
                    neighbors[r][c].append([r+1,n+1])
                    neighbors[r][c].append([n+1,c+1])
    while(True) :
        #initialize the domain
        square_domains = [[[i+1 for i in range(rows)] for j in range(cols)] for k in range(size)]

        #improvement on the domain if it founds a cage of 1 value then the domain is only this specific value
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

        #(GAMESIZE)**(GAMESIZE**2) * GAMESIZE**2 this equation indicates all possible number of values can be assigned if it excceds the limit
        if(evaluate >= Possibilities) :
            print('couldn\'t find value ')
            break
        #if there is failure then repeat the loop else break and output the value
        if(csp_BT != 'failure') :
            break 
    print(evaluate)
    return csp_BT

 


           
# Assignment =  solveGame(3, [[[3, 1], [3, 2]], [[2, 3], [2, 2]], [[2, 1], [1, 1], [1, 2], [1, 3]], [[3, 3]]] , [{'topleft': [3, 1], 'op': 'x', 'constraint_value': 3}, {'topleft': [2, 2], 'op': 'x', 'constraint_value': 6}, {'topleft': [1, 1], 'op': 'x', 'constraint_value': 6}, {'topleft': [3, 3], 'op': ' ', 'constraint_value': 2}], 0)                 
# print('Assignment : ' ,Assignment)   


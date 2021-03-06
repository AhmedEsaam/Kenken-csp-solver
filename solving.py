import random
import copy

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

    #this is for certain process where there is x , + 
    #it tries to find out if the remaining is only one value so that we can calculate the next domain which will be only one value
    if(res==-1):
        return domains

    c=cell_idx_
    if(len(c)) :
        c1=cell_idx_[0]-1
        c2=cell_idx_[1]-1
    
    # change domains of cells in same row and col
    row = x[0]
    col = x[1]
    for i in range(GAMESIZE) : 
        if (i != col) :
            if ((v in domains[row][i]) and (Assignment[row][i] == 0)):
               domains[row][i].remove(v) 
        if (i != row) :
            if ((v in domains[i][col]) and (Assignment[i][col] == 0)): 
               domains[i][col].remove(v)

    # change domains of cells in same cage
    cage = CAGES[idx_]
    cnst_v = constraint_value

    for cell in cage:
        row_next = cell[0]-1
        col_next = cell[1]-1

        #only accept the other cells (not the current one) .
        if (((row != row_next) or (col != col_next)) and (Assignment[row_next][col_next] == 0)) :
            domain_modified = 0
            if (op == '-'):
                next_domain = []
                #initially there is no domain , then we append the value that can be used in any order to get the constraint value
                if (v - cnst_v > 0):
                    if ((v - cnst_v) in domains[row_next][col_next]) :
                        next_domain.append(v - cnst_v)
                        domain_modified = 1
                    if ((v + cnst_v) in domains[row_next][col_next]) :
                        next_domain.append(v + cnst_v)
                        domain_modified = 1

                elif (v - cnst_v < 0):
                    if ((v + cnst_v) in domains[row_next][col_next]) :
                        next_domain = [v + cnst_v]
                        domain_modified = 1
                if domain_modified :
                    domains[row_next][col_next] = copy.deepcopy(next_domain)

            elif (op == '÷'):
                next_domain = []
                #initially there is no domain , then we append the value that can be used in any order to get the constraint value
                if (int(v / cnst_v) in domains[row_next][col_next]) :
                    next_domain.append(int(v / cnst_v))
                    domain_modified = 1
                if ((v * cnst_v) in domains[row_next][col_next]) :
                    next_domain.append(v * cnst_v)
                    domain_modified = 1
                if domain_modified :
                    domains[row_next][col_next] = copy.deepcopy(next_domain)

            #we needed it at the begining but now this is trivial but just we use it for readability purpose
            if res > 0 : 
                if (op == 'x'):
                    next_domain = domains[row_next][col_next]
                    #if the remaining is only one value then calculate this one value and put in it the needed domain
                    if(len(c)) :
                        if(row_next == c1 and col_next == c2):
                            if( (int(cnst_v/res) in next_domain)) :
                                next_domain = [int(cnst_v/res)]
                                domain_modified = 1
                            else :
                                next_domain = []
                                domain_modified = 1
                    
                    #else , add all possible values
                    else :
                        next_domain_ = copy.deepcopy(next_domain)
                        for d in next_domain_:
                            if (d > (cnst_v / res)):
                                    next_domain.remove(d)
                                    domain_modified = 1
                            elif ( ((cnst_v / res)% d) != 0) and (d != 1) :
                                    next_domain.remove(d)
                                    domain_modified = 1
                                
                    if domain_modified :
                        domains[row_next][col_next] = copy.deepcopy(next_domain)


                if (op == '+'):
                    next_domain = domains[row_next][col_next]
                    #if the remaining is only one value then calculate this one value and put in it the needed domain
                    if(len(c)) :
                        if(row_next == c1 and col_next == c2):
                            if( (cnst_v-res) in next_domain ) :
                                next_domain = [cnst_v-res]
                                domain_modified = 1
                            else :
                                next_domain = []
                                domain_modified = 1

                    #else , add all possible values
                    else:
                        next_domain_ = copy.deepcopy(next_domain)
                        for d in next_domain_:
                            if (d > (cnst_v - res)):
                                next_domain.remove(d)
                                domain_modified = 1
                    if domain_modified :
                        domains[row_next][col_next] = copy.deepcopy(next_domain)
    return domains  

def REMOVE_INCONSISTENT_VALUES(xi, xj, domains):
    removed=False
    xi_r=xi[0]-1
    xi_c=xi[1]-1
    xj_r=xj[0]-1
    xj_c=xj[1]-1
    op=''
    constraint_value=0
    same_2_sized_cage=0
    for idx, cage in enumerate(CAGES) :
        if(xi in cage) and (xj in cage) and len(cage)==2  :
            op=CONSTRAINTS[idx]['op']
            constraint_value=CONSTRAINTS[idx]['constraint_value']
            same_2_sized_cage=1
            # print(xi,xj,constraint_value,op,':', domains[xi_r][xi_c], domains[xj_r][xj_c])

    for v in domains[xi_r][xi_c]:
        satisfied=0
        for u in domains[xj_r][xj_c]:
            # check if no value in Xj satisfis the 2-sized cage constraint with this value in Xi
            if same_2_sized_cage==1:
                if op=='+':
                    if ((u+v==constraint_value) and u!=v):
                        satisfied=1
                elif op=='-':
                    if ((abs(u-v)==constraint_value) and u!=v):
                        satisfied=1
                elif op=='x':
                    if ((u*v==constraint_value) and u!=v):
                        satisfied=1
                elif op=='÷':
                    if ((int(max(u,v)/min(u,v))==constraint_value) and u!=v):
                        satisfied=1
            # check if no value in Xj equals this value of Xi
            elif u != v:
                satisfied=1
                
        if satisfied==0:
            domains[xi_r][xi_c].remove(v)
            # print('r')
            # print(domains)
            removed=True

    return removed,domains


def arc_consistency(domains, Assignment):
    global neighbors
    # X1=[1,1]
    # X2=[1,2]
    # queue_ =[[X1,X2],[X2,X1]]
    queue_ = []
    for r in range(GAMESIZE):
        for c in range(GAMESIZE):
            if Assignment[r][c] != 0:
                domains[r][c] = [Assignment[r][c]]
            for xk in neighbors[r][c]:
                xi = [r+1,c+1]
                queue_.append([xi,xk])

    while queue_ !=[]:
        [Xi,Xj]=queue_.pop()
        Xi_r=Xi[0]-1
        Xi_c=Xi[1]-1
        removed,domains=REMOVE_INCONSISTENT_VALUES(Xi, Xj,domains)
        if removed:
            if len(domains[Xi_r][Xi_c])==0:
                return False,domains
        
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
    # print('\n')
    # random.shuffle(square_domains[row][col])
   
    #domain_before store the domain before being changed
    cell_index_before = cell_index
    row_before= row
    col_before= col
    square_domains_before=copy.deepcopy(square_domains)
    for v in square_domains[row][col] :
        # print(evaluate)
        #evaluate according to number of values being tried
        evaluate+=1

        #restore the original domain before it has been changed (at this value).
        #Note : the domain is not completely reseted it is just restored to what it was at this variable.
        row= row_before
        col= col_before
        cell_index = cell_index_before

        #assign random value v from the domain
        Assignment[row][col] = v
        # print('\n', Assignment)
        
        #initialize the valid_Assignment to true (until the opposite is proved)
        valid_Assignment = True

        #valid assignment checking ---------------------------------------------------------------------------------------------   

        if(valid_Assignment == True):
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
            if ((technique=="FC") and valid_Assignment == True):
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
                    if( (res > constraint_value) or (constraint_value % res != 0)):
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
                        if (len(domains[i][j]) == 0) and (Assignment[i][j] == 0 ) :
                            valid_Assignment = False
                            br=1
                            break
                    if(br==1):
                        break
            
            # Check Arc Consistency
            if (technique=="AC" and valid_Assignment == True):
                x = [row,col]
                consistency,domains = arc_consistency(square_domains, Assignment)
                square_domains = domains
                # print(square_domains)
                if consistency == False:
                    valid_Assignment = False 

        #Check valid_Assignment (all constraints except if the cage is not full assign true) -------------------------------------------------------------------------
        if(valid_Assignment == True):
                # print(square_domains)
                #call next index (according to most constraining heuristic)
                if(cell_index < (size*size)-1):
                    cell_index += 1
                    row =cages_h[cell_index][0]-1
                    col =cages_h[cell_index][1]-1 

                # choose cell with minimum domain in the cage
                for cage in (CAGES) :
                    if([row+1 ,col+1] in cage) :
                        least_domains_cell = []
                        for cell in cage:
                            r_ = cell[0]-1
                            c_ = cell[1]-1
                            domain = square_domains[r_][c_]
                            if ((len(domain) < len(least_domains_cell)) or (len(least_domains_cell) == 0))\
                                and Assignment[r_][c_] == 0:
                                least_domains_cell = domain
                                row = r_
                                col = c_
                        for ind, cel in enumerate(cages_h):
                            if ([row+1, col+1] == cel) and (ind != cell_index):
                                cages_h[ind] = cages_h[cell_index]
                                cages_h[cell_index] = [row+1, col+1]
                                # print('swapped')
                                break
                        break

                #make the same process for the next variable
                result = CSP_BACKTRACKING(Assignment, square_domains)
                

                #if no failure happens return result else look for another value v in squared domain
                if result !=  'failure':
                    return result

        Assignment[row][col] = 0
        square_domains=copy.deepcopy(square_domains_before)
        # print('before:', square_domains)

        
    square_domains=copy.deepcopy(square_domains_before)
    Assignment[row_before][col_before] = 0
    #the failure indicate termination of this process so we have to get back to the root of recursion and try different values
    # print('failure')

    return 'failure'


def solveGame(GAMESIZE_, CAGES_, CONSTRAINTS_, technique_, heuristic_): # TO BE CHANGED TO A CSP SOLVER
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
    cages_h=copy.deepcopy(CAGES)
    if heuristic_ == 'MCV': 
        cages_h.sort(key = len, reverse = True)

    temp=[]
    for cage in cages_h :
        for cell in cage :
            temp.append(cell)  
    cages_h=temp
        
    evaluate=0
    Possibilities=(GAMESIZE)**(GAMESIZE**2) #Possibilities of all boards

    # Get row and col neighbours of every cell
    neighbors =[[[] for j in range(cols)] for k in range(size)]
    for r in range(GAMESIZE):
        for c in range(GAMESIZE):
            for n in range(GAMESIZE):
                if (n!=c) or (n!=r):
                    if (r,n)!=(r,c):
                        neighbors[r][c].append([r+1,n+1])
                    if (n,c)!=(r,c):
                        neighbors[r][c].append([n+1,c+1])

            # print('[',r+1,c+1,'] : ', neighbors[r][c])

    while(True) :
        #initialize the domain
        square_domains = [[[i+1 for i in range(rows)] for j in range(cols)] for k in range(size)]

        Assignment = [[0 for i in range(size)] for j in range(rows)]

        #improvement on the domain if it founds a cage of 1 value then the domain is only this specific value
        for idx, cage in enumerate(CAGES):
            if CONSTRAINTS[idx]['op'] == ' ':
                row__ =  CONSTRAINTS[idx]['topleft'][0] -1
                col__ =  CONSTRAINTS[idx]['topleft'][1] -1
                v = CONSTRAINTS[idx]['constraint_value']
                square_domains[row__][col__] = [v]
                Assignment[row__][col__] = v

                for i in range(GAMESIZE) : 
                    if (i != col__) :
                        if ((v in square_domains[row__][i]) and (Assignment[row__][i] == 0)):
                            square_domains[row__][i].remove(v) 
                    if (i != row__) :
                        if ((v in square_domains[i][col__]) and (Assignment[i][col__] == 0)): 
                            square_domains[i][col__].remove(v)
        # print(square_domains)
        # for r in range(GAMESIZE):
        #         for c in range(GAMESIZE):
        #             random.shuffle(square_domains[r][c])

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
        else:
            for r in range(GAMESIZE):
                for c in range(GAMESIZE):
                    random.shuffle(square_domains[r][c])
            print('failure')
    print(evaluate)
    num_assignments = evaluate
    return csp_BT, num_assignments

 

''' 3*3 test example 
Assignment, _ =  solveGame(3, [[[3, 2], [3, 3], [2, 3]], [[1, 2], [1, 3]], [[2, 1], [2, 2]], [[3, 1]], [[1, 1]]]\
     , [{'topleft': [2, 3], 'op': 'x', 'constraint_value': 4}, {'topleft': [1, 2], 'op': 'x', 'constraint_value': 3}, {'topleft': [2, 1], 'op': '÷', 'constraint_value': 3}, {'topleft': [3, 1], 'op': ' ', 'constraint_value': 3}, {'topleft': [1, 1], 'op': ' ', 'constraint_value': 2}]\
     , 'FC')                 
print('Assignment : ' ,Assignment)  
#'''

''' 4*4 test example
Assignment, _ =  solveGame(4, [[[3, 2], [3, 3], [3, 4], [4, 4]], [[1, 4], [1, 3]], [[2, 2], [2, 3], [2, 4]], [[3, 1], [4, 1], [4, 2], [4, 3]], [[1, 1], [1, 2]], [[2, 1]]] \
    ,[{'topleft': [3, 2], 'op': 'x', 'constraint_value': 18}, {'topleft': [1, 3], 'op': '+', 'constraint_value': 6}, {'topleft': [2, 2], 'op': 'x', 'constraint_value': 8}, {'topleft': [3, 1], 'op': 'x', 'constraint_value': 32}, {'topleft': [1, 1], 'op': 'x', 'constraint_value': 3}, {'topleft': [2, 1], 'op': ' ', 'constraint_value': 3}]\
    ,'FC')                 
print('Assignment : ' ,Assignment)   
#'''
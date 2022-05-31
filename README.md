# Kenken-csp-solver
Exploring ho to solve Kenken games using CSP techniques.<br>

## Game generator
Generate new game.<br>

## CSP-solver solve using following techniques : <br> <br>
### 1- Backtracking : <br>
Assign values from the domain and checking the constraints if it fail it check another value from the domain , until it ends the domain  only at this time it return 'failure' and try another set of values (same domains different order) . <br>
if it finishes assignment without failure then this is the answer <br> <br>
### 2- Backtracking with forward checking  : <br>
similarily assign values from the domain until it is done , but whenever it assign a value it modify the domain of the surrounding value according to following constraints :- <br>
1- First constraint : No repeated values in same row and cloumn . <br>
2- Second constraint : the operation made on the cage satisfy the condition . <br> <br>

## 3- Backtracking with arc consistency  : <br>
At every assignment, exclude any value in the domain which has not a value in the other end of the constraint that both satisfy it.
We check the two ends of binary constraints which include:
- No repeated values in same row and cloumn.
- Each two ends' domains of 2-sized cages satisfy the constraint value and operation.

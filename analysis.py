from time import time
from new_game import generateNewGame
from solving import solveGame
from csv import writer

file = open('out.csv', 'w')
writer = writer(file, dialect='excel')
writer.writerow(["Technique", "Size", "Assignments", "time_elapsed"])

techniques = ['BT', 'FC', 'AC']
heuristics = ['None', 'MCV']  # MCV: Most Constraining Variable
MAX_SIZE = 4

for n in range(1, MAX_SIZE):
    for i in range(2):
         # Generate new game
        size = n+1
        game, cages, constraints = generateNewGame(size)
        for technique in techniques:
            for heuristic in heuristics:
                solved = 'failure'
                while (solved == 'failure'):
                    # solve and record time elapsed
                    t = time()
                    solved, assignments = solveGame(size, cages, constraints, technique, heuristic)
                    time_elapsed = time() - t

                Algorithm = technique
                if heuristic != 'None':
                    Algorithm = technique + ' with ' + heuristic
                writer.writerow([Algorithm, size, assignments, time_elapsed])

file.close()

from time import time
from new_game import generateNewGame
from solving import solveGame
from csv import writer

file = open('out.csv', 'w')
writer = writer(file, dialect='excel')
writer.writerow(["Technique", "Size", "Assignments", "time_elapsed"])

techniques = ['BT', 'FC', 'AC']
MAX_SIZE = 5
for technique in techniques:
    for n in range(1, MAX_SIZE):
        for i in range(4):
            solved = 'failure'
            while (solved == 'failure'):
                # Generate new game
                size = n+1
                game, cages, constraints = generateNewGame(size)
                # solve and record time elapsed
                t = time()
                solved, assignments = solveGame(size, cages, constraints, technique)
                time_elapsed = time() - t

            writer.writerow([technique, size, assignments, time_elapsed])

file.close()

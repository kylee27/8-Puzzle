from itertools import count

expanded = []

def printBoard(board):
    for i in range(3):
        for j in range(3):
            print(board[i*3 + j], end=' ')
        print()
    print()

def genChild(board):
    children = []
    # row and col of the zero tile
    newRow, newCol = board.index(0)//3, board.index(0)%3
    
    def swap(r, c):
        child = board[:]
        child[newRow*3+newCol], child[r*3+c] = child[r*3+c], child[newRow*3+newCol]
        return child

    # moving up
    if newRow > 0: children.append(swap(newRow-1, newCol))
    # moving down
    if newRow < 2: children.append(swap(newRow+1, newCol))
    # moving right
    if newCol < 2: children.append(swap(newRow, newCol+1))
    # moving left
    if newCol > 0: children.append(swap(newRow, newCol-1))

    return children


# returns the path from startState to goalState if any
def dfs(path, goalState, depth):
    global expanded

    if depth == 0: return
    if path[-1] == goalState: return path

    expanded.append(path[-1])
    # generate at most four children
    for child in genChild(path[-1]):
        newPath = dfs(path+[child], goalState, depth-1)
        if newPath and newPath!=0: return newPath
    if len(expanded) > 1000000: return 0
    

def ids(startState, goalState):
    for depth in count():
        print("Depth:", depth, end="")
        path = dfs([startState], goalState, depth)
        # return path if goalState is reached at depth
        if path==0: return 0
        if path: return path
        print("\tNodes expanded:", len(expanded))
        

# deal with input
startState = input("Enter start state as a string: ")
if not startState: startState = [7, 2, 4, 5, 0, 6, 8, 3, 1]
else: 
    startState = [*startState]
    for i in range(len(startState)):
        startState[i] = int(startState[i])
goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
print("\nSolving 8-puzzle problem with Iterative Deepening Search. ")
print("Initial State: ")
print(startState)
result = ids(startState, goalState)
if result==0: print("\tTerminated\nOne million nodes expanded. \nNo successful paths found. ")
elif result: 
    print("Found\nSuccessful path found! \nNodes expanded:", len(expanded), "\n\nPath: ")
    for i, j in enumerate(result): 
        print("Move:", i, " " if i<10 else "", j)
        printBoard(j)
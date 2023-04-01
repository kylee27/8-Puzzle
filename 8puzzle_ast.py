from itertools import count

def printBoard(board):
    for i in range(3):
        for j in range(3):
            print(board[i*3 + j], end=' ')
        print()
    print()

def genChild(board):
    children = []
    board = list(board)
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

# heuristics
# calculate number of misplaced tiles
def h1(board): 
    cost = 0
    for i in board:
        if i != 0 and board[i] != i: cost+=1
    return cost

# total Manhattan distance
def h2(board):
    cost = 0
    for i, j in enumerate(board):
        if j == 0: continue
        temp = 0
        while i//3 != j//3:
            temp += 1
            j += 3 if j<i else -3
        while j-i != 0:
            temp += 1
            j += 1 if j<i else -1
        cost += temp
    return cost


def ast(startState, goalState, heuristic):

    global expanded
    reached = [startState, ]
    parents = {startState : None}
    gn = {startState : 0}
    global fn
    fn = {startState : 0}

    while len(reached) != 0:
        if goalState in reached:
            path = []
            current = reached[reached.index(goalState)]
            while current != startState:
                path.append(current)
                current = parents[current]
            return [startState] + path[::-1]
        
        reached.sort(key=lambda x: fn[x])
        node = reached.pop(0)
        expanded.add(node)
        
        for child in genChild(node):
            child = tuple(child)
            if child in expanded: continue
            if child not in reached:
                parents[child] = node
                gn[child] = gn[node] + 1
                fn[child] = gn[node] + 1 + (h1(child) if heuristic == "h1" else h2(child))
                reached.append(child)

    return None


# deal with input
startState = input("Enter start state as a string: ")
if not startState: startState = [7, 2, 4, 5, 0, 6, 8, 3, 1]
else: 
    startState = [*startState]
    for i in range(len(startState)):
        startState[i] = int(startState[i])
goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]

expanded = set()
print("\nSolving 8-puzzle problem with A* Search. ")
print("Heuristic h1: Misplaced Tiles")
print("Initial State: ")
print(startState)
printBoard(startState)

result = ast(tuple(startState), tuple(goalState), "h1")
if result: 
    print("Successful path found by h1: Misplaced Tiles!")
    print("Nodes expanded:", len(expanded), "\n\nPath: \n")
    for i, j in enumerate(result): 
        print("Move:", i, " " if i<10 else "", list(j))
        printBoard(j)
else: 
    print("No successful path found by h1: Misplaced Tiles. ")

print("\n###############################################\n")

expanded = set()
print("Solving 8-puzzle problem with A* Search. ")
print("Heuristic h2: Manhattan Distance")
print("Initial State: ")
print(startState)
printBoard(startState)
result = ast(tuple(startState), tuple(goalState), "h2")
if result: 
    print("Successful path found by h2: Manhattan Distance!")
    print("Nodes expanded:", len(expanded), "\n\nPath: \n")
    for i, j in enumerate(result): 
        print("Move:", i, " " if i<10 else "", list(j))
        printBoard(j)
else: 
    print("No successful path found by h2: Manhattan Distance. ")
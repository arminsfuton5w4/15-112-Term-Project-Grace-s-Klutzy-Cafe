def DFS(adjacencyList, state, s, v):
    b,target,L=state
    if v in s:
        return revisit(state, v)
    else:
        state=visit(state, v)
        s.add(v)
        for neighbor in adjacencyList.get(v,[]):
            state=DFS(adjacencyList, state, s, neighbor)
        state=finish(state, v)
    return state

def visit(state, v): 
    b,target,L=state
    if not b:
        L.append(v)
    if v in target:
        b=True
    return (b, target, L)
    
def revisit(state, v):
    return state

def finish(state, v):
    return state

def makeAdjacencyList():
    adjList=dict()
    for row in range(4):
        for col in range(12):
            #four edge case: corners: 2 edges
            if row==0 and col==0:
                adjList[(row,col)]={(row+1, col), (row, col+1)}
            elif row==0 and col==11:
                adjList[(row,col)]={(row+1, col), (row, col-1)}
            elif row==3 and col==0:
                adjList[(row,col)]={(row-1, col), (row, col+1)}
            elif row==3 and col==11:
                adjList[(row,col)]={(row-1, col), (row, col-1)}
            #sides of the board: 3 edges
            elif row==0:
                adjList[(row,col)]={(row+1, col), (row, col-1), (row, col+1)}
            elif col==0:
                adjList[(row,col)]={(row-1, col), (row+1, col), (row, col+1)}
            elif row==3:
                adjList[(row,col)]={(row-1, col), (row, col-1), (row, col+1)}
            elif col==11:
                adjList[(row,col)]={(row-1, col), (row+1, col), (row, col-1)}
            #everything else: 4 edges
            else:
                adjList[(row, col)]={(row-1, col), (row+1, col), (row, col-1), (row, col+1)}
    return adjList

board=makeAdjacencyList()
tables=[(0,4),(0,5),(1,4),(1,5), (2,1),(2,2),(3,1),(3,2), (2,7),(2,8),(3,7),(3,8)]
visited=set()
state=(False, tables, [])
DFS(board, state, visited, (0,9))
print(state[-1])
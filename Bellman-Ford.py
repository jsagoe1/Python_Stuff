
# =============================================================================
# Graph implemented as adjacency list with dictionay
# =============================================================================
graph = {

'A':{'E':-3},
'B':{'C':7},
'C':{'F':-5},
'E':{'B':1, 'G':6, 'H':-3},
'F':{'B':8},
'G':{'D':2},
'H':{'G':1},
'S':{'A':2},
}



def bellmanFord(graph, start, goal):
    # check if start is same as goal
    if start in graph and start == goal:
        return ([start], 0)
    # check if start or goal not present in graph
    if start not in graph:
        print("Error:'start' not present in graph")
        return ([],0)
        
    infinity = float('inf')         #Infinity
    shortestDistanceFromStart = {}  # to hold shortest distance to each vertex
    prevVertex = {}                 # to keep track of vertices leading to curVertex
    
    #set all vertices to infinity initially to start with
    for vertex in graph:
        #this for loop makes sure it includes D since D has no leaving path
        for edge,weight in graph[vertex].items():
            shortestDistanceFromStart[edge] = infinity
    #except start vertex, set to 0
    shortestDistanceFromStart[start] = 0
    
    prevVertex[start] = None          # start has no prev node, so set to None
    
    #repeat (no. of vertices times)
    for iter in range(len(shortestDistanceFromStart)):
        for vertex in graph:
            #go through all edges for each vertex 
            for edge, weight in graph[vertex].items():
                #vertex in this case will be predecessor of current edge
                distance = shortestDistanceFromStart[vertex] + weight     
                if distance < shortestDistanceFromStart[edge]:
                    shortestDistanceFromStart[edge] = distance
                    prevVertex[edge] = vertex
        

    path = []                       # to trace path
    cur = goal                      # start from goal and trace back
    while cur!=None:
        if cur not in prevVertex:   #no path from start to goal
            print("No path from start to goal")
            return ([], 0)
        path.insert(0,cur)
        cur = prevVertex[cur]
    return (path, shortestDistanceFromStart[goal])
    
    
print(bellmanFord(graph, 'S', 'D'))
